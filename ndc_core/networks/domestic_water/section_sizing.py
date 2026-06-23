from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Mapping

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.domain.appliances import Appliance
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import SectionUsageContext
from ndc_core.domain.pipes import PipeSize
from ndc_core.hydraulics.pipe_sizing import select_pipe_size_by_velocity
from ndc_core.hydraulics.velocity import velocity_from_l_s_and_mm
from ndc_core.networks.domestic_water.demand import DomesticWaterDemandBuilder
from ndc_core.networks.domestic_water.profiles import (
    COLD_WATER_PROFILE,
    HOT_WATER_PROFILE,
    DomesticWaterProfile,
)
from ndc_core.networks.domestic_water.types import (
    DomesticWaterDemand,
    DomesticWaterSide,
)
from ndc_core.networks.domestic_water.appliance_counts import normalize_appliance_counts
from ndc_core.networks.domestic_water.entity_access import clean_optional_code


class SectionSizingMode(StrEnum):
    """Section diameter selection mode."""

    AUTOMATIC = "automatic"
    FORCED_PIPE = "forced_pipe"
    FORCED_INTERNAL_DIAMETER = "forced_internal_diameter"


@dataclass(frozen=True, slots=True)
class DomesticWaterSectionSizing:
    """Sizing result for one domestic water section."""

    section_id: str
    side: DomesticWaterSide
    mode: SectionSizingMode
    demand: DomesticWaterDemand
    selected_pipe_size: PipeSize | None
    selected_pipe_size_code: str | None
    theoretical_internal_diameter_mm: float | None
    min_required_internal_diameter_mm: float | None
    used_internal_diameter_mm: float | None
    velocity_m_s: float | None
    max_velocity_m_s: float
    velocity_ok: bool | None
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @property
    def sized(self) -> bool:
        return self.used_internal_diameter_mm is not None

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)


@dataclass(frozen=True, slots=True)
class DomesticWaterSectionSizingEngine:
    """
    Common EFS/ECS forward section sizing engine.

    This engine computes demand, selects or applies a diameter, then writes
    sizing state back to the Section object for future pressure loss engines.
    """

    appliance_catalog: ApplianceCatalog
    pipe_catalog: PipeCatalog
    profile: DomesticWaterProfile

    @classmethod
    def cold_water(
        cls,
        appliance_catalog: ApplianceCatalog,
        pipe_catalog: PipeCatalog,
    ) -> DomesticWaterSectionSizingEngine:
        return cls(
            appliance_catalog=appliance_catalog,
            pipe_catalog=pipe_catalog,
            profile=COLD_WATER_PROFILE,
        )

    @classmethod
    def hot_water(
        cls,
        appliance_catalog: ApplianceCatalog,
        pipe_catalog: PipeCatalog,
    ) -> DomesticWaterSectionSizingEngine:
        return cls(
            appliance_catalog=appliance_catalog,
            pipe_catalog=pipe_catalog,
            profile=HOT_WATER_PROFILE,
        )

    def size_section_from_counts(
        self,
        section: Section,
        appliance_counts: Mapping[str, int],
        *,
        max_velocity_m_s: float | None = None,
    ) -> Result[DomesticWaterSectionSizing]:
        messages: list[EngineMessage] = []

        demand_result = DomesticWaterDemandBuilder(
            appliance_catalog=self.appliance_catalog,
            profile=self.profile,
        ).compute_from_counts(appliance_counts)

        messages.extend(demand_result.messages)

        if demand_result.value is None:
            return Result.failure(messages=messages)

        demand = demand_result.value
        velocity_limit = max_velocity_m_s or velocity_limit_for_context(
            section.usage_context
        )

        raw_counts = normalize_appliance_counts(appliance_counts)
        effective_counts = {
            item.appliance_code: item.effective_count
            for item in demand.items
            if item.effective_count > 0
        }

        min_required_diameter = max(
            _minimum_appliance_internal_diameter_mm(
                appliance_catalog=self.appliance_catalog,
                appliance_counts=raw_counts,
                profile=self.profile,
            ),
            0.0,
        )

        if demand.design_flow_l_s <= 0.0:
            messages.append(
                EngineMessage.warning(
                    code="DOMESTIC_WATER_SECTION_NO_FLOW",
                    text="Section demand is zero; diameter sizing was not performed.",
                    context={"section_id": section.id},
                )
            )
            sizing = DomesticWaterSectionSizing(
                section_id=section.id,
                side=self.profile.side,
                mode=SectionSizingMode.AUTOMATIC,
                demand=demand,
                selected_pipe_size=None,
                selected_pipe_size_code=None,
                theoretical_internal_diameter_mm=None,
                min_required_internal_diameter_mm=(
                    min_required_diameter or None
                ),
                used_internal_diameter_mm=None,
                velocity_m_s=None,
                max_velocity_m_s=velocity_limit,
                velocity_ok=None,
                messages=tuple(messages),
            )
            _apply_sizing_to_section(
                section=section,
                sizing=sizing,
                raw_counts=raw_counts,
                effective_counts=effective_counts,
            )
            return Result.partial(value=sizing, messages=messages)

        sizing = self._select_or_force_diameter(
            section=section,
            demand=demand,
            raw_counts=raw_counts,
            effective_counts=effective_counts,
            min_required_diameter_mm=min_required_diameter,
            max_velocity_m_s=velocity_limit,
            messages=messages,
        )

        _apply_sizing_to_section(
            section=section,
            sizing=sizing,
            raw_counts=raw_counts,
            effective_counts=effective_counts,
        )

        if sizing.has_errors:
            return Result.failure(value=sizing, messages=messages)

        return Result.success(value=sizing, messages=messages)

    def _select_or_force_diameter(
        self,
        section: Section,
        demand: DomesticWaterDemand,
        raw_counts: dict[str, int],
        effective_counts: dict[str, int],
        min_required_diameter_mm: float,
        max_velocity_m_s: float,
        messages: list[EngineMessage],
    ) -> DomesticWaterSectionSizing:
        forced_pipe_code = clean_optional_code(section.forced_pipe_size_code)
        forced_diameter = _positive_optional_float(
            section.forced_internal_diameter_mm
        )

        if forced_pipe_code:
            return self._size_with_forced_pipe(
                section=section,
                demand=demand,
                forced_pipe_code=forced_pipe_code,
                min_required_diameter_mm=min_required_diameter_mm,
                max_velocity_m_s=max_velocity_m_s,
                messages=messages,
            )

        if forced_diameter is not None:
            return self._size_with_forced_internal_diameter(
                section=section,
                demand=demand,
                forced_diameter_mm=forced_diameter,
                min_required_diameter_mm=min_required_diameter_mm,
                max_velocity_m_s=max_velocity_m_s,
                messages=messages,
            )

        return self._size_automatically(
            section=section,
            demand=demand,
            raw_counts=raw_counts,
            effective_counts=effective_counts,
            min_required_diameter_mm=min_required_diameter_mm,
            max_velocity_m_s=max_velocity_m_s,
            messages=messages,
        )

    def _size_automatically(
        self,
        section: Section,
        demand: DomesticWaterDemand,
        raw_counts: dict[str, int],
        effective_counts: dict[str, int],
        min_required_diameter_mm: float,
        max_velocity_m_s: float,
        messages: list[EngineMessage],
    ) -> DomesticWaterSectionSizing:
        del raw_counts, effective_counts

        pipe_sizes = self.pipe_catalog.list_sizes_for_material(
            section.fluid_code
        )
        if not pipe_sizes:
            pipe_sizes = self.pipe_catalog.list_sizes_for_material(
                section.fluid_code.lower()
            )
        if not pipe_sizes:
            pipe_sizes = list(self.pipe_catalog.sizes_by_code.values())

        hydraulic_result = select_pipe_size_by_velocity(
            design_flow_l_s=demand.design_flow_l_s,
            pipe_sizes=pipe_sizes,
            max_velocity_m_s=max_velocity_m_s,
            min_internal_diameter_mm=(
                min_required_diameter_mm or None
            ),
        )

        selected = hydraulic_result.selected_pipe_size

        if selected is None:
            messages.append(
                EngineMessage.error(
                    code="DOMESTIC_WATER_NO_PIPE_SIZE_FOUND",
                    text="No usable pipe size was found for section sizing.",
                    context={"section_id": section.id},
                )
            )

        return DomesticWaterSectionSizing(
            section_id=section.id,
            side=self.profile.side,
            mode=SectionSizingMode.AUTOMATIC,
            demand=demand,
            selected_pipe_size=selected,
            selected_pipe_size_code=selected.code if selected else None,
            theoretical_internal_diameter_mm=(
                hydraulic_result.theoretical_internal_diameter_mm
            ),
            min_required_internal_diameter_mm=(
                min_required_diameter_mm or None
            ),
            used_internal_diameter_mm=(
                selected.internal_diameter_mm if selected else None
            ),
            velocity_m_s=hydraulic_result.real_velocity_m_s,
            max_velocity_m_s=max_velocity_m_s,
            velocity_ok=hydraulic_result.velocity_ok,
            messages=tuple(messages),
        )

    def _size_with_forced_pipe(
        self,
        section: Section,
        demand: DomesticWaterDemand,
        forced_pipe_code: str,
        min_required_diameter_mm: float,
        max_velocity_m_s: float,
        messages: list[EngineMessage],
    ) -> DomesticWaterSectionSizing:
        selected = self.pipe_catalog.get_size(forced_pipe_code)

        if selected is None:
            messages.append(
                EngineMessage.error(
                    code="DOMESTIC_WATER_FORCED_PIPE_UNKNOWN",
                    text="Forced pipe size code is not defined in the pipe catalog.",
                    context={
                        "section_id": section.id,
                        "forced_pipe_size_code": forced_pipe_code,
                    },
                )
            )
            used_diameter = None
            velocity = None
            velocity_ok = None
        else:
            used_diameter = selected.internal_diameter_mm
            velocity = velocity_from_l_s_and_mm(
                demand.design_flow_l_s,
                used_diameter,
            )
            velocity_ok = velocity <= max_velocity_m_s if velocity > 0.0 else None

            if (
                min_required_diameter_mm > 0.0
                and used_diameter < min_required_diameter_mm
            ):
                messages.append(
                    EngineMessage.warning(
                        code="DOMESTIC_WATER_FORCED_PIPE_BELOW_MIN_DIAMETER",
                        text=(
                            "Forced pipe internal diameter is below appliance "
                            "minimum diameter."
                        ),
                        context={
                            "section_id": section.id,
                            "forced_pipe_size_code": forced_pipe_code,
                            "used_internal_diameter_mm": used_diameter,
                            "min_required_internal_diameter_mm": (
                                min_required_diameter_mm
                            ),
                        },
                    )
                )

            if velocity_ok is False:
                messages.append(
                    EngineMessage.warning(
                        code="DOMESTIC_WATER_FORCED_PIPE_VELOCITY_EXCEEDED",
                        text="Forced pipe velocity exceeds the maximum velocity.",
                        context={
                            "section_id": section.id,
                            "velocity_m_s": velocity,
                            "max_velocity_m_s": max_velocity_m_s,
                        },
                    )
                )

        theoretical = select_pipe_size_by_velocity(
            design_flow_l_s=demand.design_flow_l_s,
            pipe_sizes=self.pipe_catalog.sizes_by_code.values(),
            max_velocity_m_s=max_velocity_m_s,
            min_internal_diameter_mm=(
                min_required_diameter_mm or None
            ),
        ).theoretical_internal_diameter_mm

        return DomesticWaterSectionSizing(
            section_id=section.id,
            side=self.profile.side,
            mode=SectionSizingMode.FORCED_PIPE,
            demand=demand,
            selected_pipe_size=selected,
            selected_pipe_size_code=selected.code if selected else None,
            theoretical_internal_diameter_mm=theoretical,
            min_required_internal_diameter_mm=(
                min_required_diameter_mm or None
            ),
            used_internal_diameter_mm=used_diameter,
            velocity_m_s=velocity,
            max_velocity_m_s=max_velocity_m_s,
            velocity_ok=velocity_ok,
            messages=tuple(messages),
        )

    def _size_with_forced_internal_diameter(
        self,
        section: Section,
        demand: DomesticWaterDemand,
        forced_diameter_mm: float,
        min_required_diameter_mm: float,
        max_velocity_m_s: float,
        messages: list[EngineMessage],
    ) -> DomesticWaterSectionSizing:
        velocity = velocity_from_l_s_and_mm(
            demand.design_flow_l_s,
            forced_diameter_mm,
        )
        velocity_ok = velocity <= max_velocity_m_s if velocity > 0.0 else None

        if (
            min_required_diameter_mm > 0.0
            and forced_diameter_mm < min_required_diameter_mm
        ):
            messages.append(
                EngineMessage.warning(
                    code="DOMESTIC_WATER_FORCED_DIAMETER_BELOW_MIN_DIAMETER",
                    text=(
                        "Forced internal diameter is below appliance minimum "
                        "diameter."
                    ),
                    context={
                        "section_id": section.id,
                        "forced_internal_diameter_mm": forced_diameter_mm,
                        "min_required_internal_diameter_mm": (
                            min_required_diameter_mm
                        ),
                    },
                )
            )

        if velocity_ok is False:
            messages.append(
                EngineMessage.warning(
                    code="DOMESTIC_WATER_FORCED_DIAMETER_VELOCITY_EXCEEDED",
                    text="Forced internal diameter velocity exceeds the limit.",
                    context={
                        "section_id": section.id,
                        "velocity_m_s": velocity,
                        "max_velocity_m_s": max_velocity_m_s,
                    },
                )
            )

        theoretical = select_pipe_size_by_velocity(
            design_flow_l_s=demand.design_flow_l_s,
            pipe_sizes=self.pipe_catalog.sizes_by_code.values(),
            max_velocity_m_s=max_velocity_m_s,
            min_internal_diameter_mm=(
                min_required_diameter_mm or None
            ),
        ).theoretical_internal_diameter_mm

        return DomesticWaterSectionSizing(
            section_id=section.id,
            side=self.profile.side,
            mode=SectionSizingMode.FORCED_INTERNAL_DIAMETER,
            demand=demand,
            selected_pipe_size=None,
            selected_pipe_size_code=None,
            theoretical_internal_diameter_mm=theoretical,
            min_required_internal_diameter_mm=(
                min_required_diameter_mm or None
            ),
            used_internal_diameter_mm=forced_diameter_mm,
            velocity_m_s=velocity,
            max_velocity_m_s=max_velocity_m_s,
            velocity_ok=velocity_ok,
            messages=tuple(messages),
        )


def size_cold_water_section_from_counts(
    section: Section,
    appliance_counts: Mapping[str, int],
    appliance_catalog: ApplianceCatalog,
    pipe_catalog: PipeCatalog,
    *,
    max_velocity_m_s: float | None = None,
) -> Result[DomesticWaterSectionSizing]:
    """Convenience function for EFS section sizing."""

    return DomesticWaterSectionSizingEngine.cold_water(
        appliance_catalog=appliance_catalog,
        pipe_catalog=pipe_catalog,
    ).size_section_from_counts(
        section,
        appliance_counts,
        max_velocity_m_s=max_velocity_m_s,
    )


def size_hot_water_section_from_counts(
    section: Section,
    appliance_counts: Mapping[str, int],
    appliance_catalog: ApplianceCatalog,
    pipe_catalog: PipeCatalog,
    *,
    max_velocity_m_s: float | None = None,
) -> Result[DomesticWaterSectionSizing]:
    """Convenience function for ECS forward section sizing."""

    return DomesticWaterSectionSizingEngine.hot_water(
        appliance_catalog=appliance_catalog,
        pipe_catalog=pipe_catalog,
    ).size_section_from_counts(
        section,
        appliance_counts,
        max_velocity_m_s=max_velocity_m_s,
    )


def velocity_limit_for_context(
    usage_context: SectionUsageContext | str | None,
) -> float:
    """
    Return default velocity limit for domestic water.

    Current DTU-oriented defaults:
    - basement / technical room: 2.0 m/s
    - riser: 1.5 m/s
    - other distribution contexts: 2.0 m/s
    """

    value = (
        usage_context.value
        if isinstance(usage_context, SectionUsageContext)
        else str(usage_context or "")
    )
    key = value.strip().lower()

    if key in {
        SectionUsageContext.RISER.value,
        SectionUsageContext.DWELLING.value,
    }:
        return 1.5

    return 2.0


def _apply_sizing_to_section(
    *,
    section: Section,
    sizing: DomesticWaterSectionSizing,
    raw_counts: dict[str, int],
    effective_counts: dict[str, int],
) -> None:
    section.flow_l_s = sizing.demand.design_flow_l_s
    section.velocity_m_s = sizing.velocity_m_s

    section.downstream_appliance_counts.clear()
    section.downstream_appliance_counts.update(raw_counts)

    section.effective_appliance_counts.clear()
    section.effective_appliance_counts.update(effective_counts)

    section.selected_pipe_size_code = sizing.selected_pipe_size_code
    section.selected_internal_diameter_mm = sizing.used_internal_diameter_mm


def _minimum_appliance_internal_diameter_mm(
    *,
    appliance_catalog: ApplianceCatalog,
    appliance_counts: Mapping[str, int],
    profile: DomesticWaterProfile,
) -> float:
    minimum = 0.0

    for code, count in appliance_counts.items():
        if count <= 0:
            continue

        appliance = appliance_catalog.get(code)
        if appliance is None:
            continue

        if _flow_for_profile(appliance, profile) <= 0.0:
            continue

        if appliance.min_internal_diameter_mm is None:
            continue

        try:
            diameter = float(appliance.min_internal_diameter_mm)
        except (TypeError, ValueError):
            continue

        if diameter > minimum:
            minimum = diameter

    return minimum


def _flow_for_profile(
    appliance: Appliance,
    profile: DomesticWaterProfile,
) -> float:
    value = getattr(appliance, profile.flow_attribute_name, 0.0)

    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return 0.0


def _positive_optional_float(value: Any) -> float | None:
    if value is None:
        return None

    try:
        number = float(value)
    except (TypeError, ValueError):
        return None

    if number <= 0.0:
        return None

    return number