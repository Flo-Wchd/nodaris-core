from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import SectionUsageContext
from ndc_core.networks.domestic_water.demand import DomesticWaterDemandBuilder
from ndc_core.networks.domestic_water.profiles import (
    COLD_WATER_PROFILE,
    HOT_WATER_PROFILE,
    DomesticWaterProfile,
)
from ndc_core.networks.domestic_water.appliance_counts import normalize_appliance_counts
from ndc_core.networks.domestic_water.section_state import apply_section_sizing_state
from ndc_core.networks.domestic_water.appliance_rules import minimum_appliance_internal_diameter_mm
from ndc_core.networks.domestic_water.section_sizing_result import (
    DomesticWaterSectionSizing,
    SectionSizingMode,
)
from ndc_core.networks.domestic_water.section_diameter_selection import (
    select_section_diameter,
)


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
            minimum_appliance_internal_diameter_mm(
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
            apply_section_sizing_state(
                section=section,
                sizing=sizing,
                raw_counts=raw_counts,
                effective_counts=effective_counts,
            )
            return Result.partial(value=sizing, messages=messages)

        sizing = select_section_diameter(
            section=section,
            demand=demand,
            pipe_catalog=self.pipe_catalog,
            side=self.profile.side,
            min_required_diameter_mm=min_required_diameter,
            max_velocity_m_s=velocity_limit,
            messages=messages,
        )

        apply_section_sizing_state(
            section=section,
            sizing=sizing,
            raw_counts=raw_counts,
            effective_counts=effective_counts,
        )

        if sizing.has_errors:
            return Result.failure(value=sizing, messages=messages)

        return Result.success(value=sizing, messages=messages)


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