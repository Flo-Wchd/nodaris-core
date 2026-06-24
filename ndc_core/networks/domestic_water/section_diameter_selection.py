from __future__ import annotations

from collections.abc import Sequence

from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.domain.networks.section import Section
from ndc_core.domain.pipes import PipeSize
from ndc_core.hydraulics.pipe_sizing import select_pipe_size_by_velocity
from ndc_core.hydraulics.velocity import velocity_from_l_s_and_mm
from ndc_core.networks.domestic_water.entity_access import clean_optional_code
from ndc_core.networks.domestic_water.numeric import positive_optional_float
from ndc_core.networks.domestic_water.section_sizing_result import (
    DomesticWaterSectionSizing,
    SectionSizingMode,
)
from ndc_core.networks.domestic_water.types import (
    DomesticWaterDemand,
    DomesticWaterSide,
)


def select_section_diameter(
    *,
    section: Section,
    demand: DomesticWaterDemand,
    pipe_catalog: PipeCatalog,
    side: DomesticWaterSide,
    min_required_diameter_mm: float,
    max_velocity_m_s: float,
    messages: list[EngineMessage],
) -> DomesticWaterSectionSizing:
    """
    Select or apply the section internal diameter.

    Selection priority:
    1. forced pipe size code;
    2. forced internal diameter;
    3. automatic pipe sizing.
    """

    forced_pipe_code = clean_optional_code(section.forced_pipe_size_code)
    forced_diameter = positive_optional_float(
        section.forced_internal_diameter_mm
    )

    if forced_pipe_code:
        return _size_with_forced_pipe(
            section=section,
            demand=demand,
            pipe_catalog=pipe_catalog,
            side=side,
            forced_pipe_code=forced_pipe_code,
            min_required_diameter_mm=min_required_diameter_mm,
            max_velocity_m_s=max_velocity_m_s,
            messages=messages,
        )

    if forced_diameter is not None:
        return _size_with_forced_internal_diameter(
            section=section,
            demand=demand,
            pipe_catalog=pipe_catalog,
            side=side,
            forced_diameter_mm=forced_diameter,
            min_required_diameter_mm=min_required_diameter_mm,
            max_velocity_m_s=max_velocity_m_s,
            messages=messages,
        )

    return _size_automatically(
        section=section,
        demand=demand,
        pipe_catalog=pipe_catalog,
        side=side,
        min_required_diameter_mm=min_required_diameter_mm,
        max_velocity_m_s=max_velocity_m_s,
        messages=messages,
    )


def _size_automatically(
    *,
    section: Section,
    demand: DomesticWaterDemand,
    pipe_catalog: PipeCatalog,
    side: DomesticWaterSide,
    min_required_diameter_mm: float,
    max_velocity_m_s: float,
    messages: list[EngineMessage],
) -> DomesticWaterSectionSizing:
    pipe_sizes = _pipe_sizes_for_section(
        pipe_catalog=pipe_catalog,
        section=section,
    )

    hydraulic_result = select_pipe_size_by_velocity(
        design_flow_l_s=demand.design_flow_l_s,
        pipe_sizes=pipe_sizes,
        max_velocity_m_s=max_velocity_m_s,
        min_internal_diameter_mm=min_required_diameter_mm or None,
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
        side=side,
        mode=SectionSizingMode.AUTOMATIC,
        demand=demand,
        selected_pipe_size=selected,
        selected_pipe_size_code=selected.code if selected else None,
        theoretical_internal_diameter_mm=(
            hydraulic_result.theoretical_internal_diameter_mm
        ),
        min_required_internal_diameter_mm=min_required_diameter_mm or None,
        used_internal_diameter_mm=(
            selected.internal_diameter_mm if selected else None
        ),
        velocity_m_s=hydraulic_result.real_velocity_m_s,
        max_velocity_m_s=max_velocity_m_s,
        velocity_ok=hydraulic_result.velocity_ok,
        messages=tuple(messages),
    )


def _size_with_forced_pipe(
    *,
    section: Section,
    demand: DomesticWaterDemand,
    pipe_catalog: PipeCatalog,
    side: DomesticWaterSide,
    forced_pipe_code: str,
    min_required_diameter_mm: float,
    max_velocity_m_s: float,
    messages: list[EngineMessage],
) -> DomesticWaterSectionSizing:
    selected = pipe_catalog.get_size(forced_pipe_code)

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

        _append_forced_pipe_warnings(
            section=section,
            forced_pipe_code=forced_pipe_code,
            used_diameter_mm=used_diameter,
            velocity_m_s=velocity,
            velocity_ok=velocity_ok,
            min_required_diameter_mm=min_required_diameter_mm,
            max_velocity_m_s=max_velocity_m_s,
            messages=messages,
        )

    theoretical = _theoretical_internal_diameter_mm(
        demand=demand,
        pipe_sizes=pipe_catalog.sizes_by_code.values(),
        min_required_diameter_mm=min_required_diameter_mm,
        max_velocity_m_s=max_velocity_m_s,
    )

    return DomesticWaterSectionSizing(
        section_id=section.id,
        side=side,
        mode=SectionSizingMode.FORCED_PIPE,
        demand=demand,
        selected_pipe_size=selected,
        selected_pipe_size_code=selected.code if selected else None,
        theoretical_internal_diameter_mm=theoretical,
        min_required_internal_diameter_mm=min_required_diameter_mm or None,
        used_internal_diameter_mm=used_diameter,
        velocity_m_s=velocity,
        max_velocity_m_s=max_velocity_m_s,
        velocity_ok=velocity_ok,
        messages=tuple(messages),
    )


def _size_with_forced_internal_diameter(
    *,
    section: Section,
    demand: DomesticWaterDemand,
    pipe_catalog: PipeCatalog,
    side: DomesticWaterSide,
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

    _append_forced_internal_diameter_warnings(
        section=section,
        forced_diameter_mm=forced_diameter_mm,
        velocity_m_s=velocity,
        velocity_ok=velocity_ok,
        min_required_diameter_mm=min_required_diameter_mm,
        max_velocity_m_s=max_velocity_m_s,
        messages=messages,
    )

    theoretical = _theoretical_internal_diameter_mm(
        demand=demand,
        pipe_sizes=pipe_catalog.sizes_by_code.values(),
        min_required_diameter_mm=min_required_diameter_mm,
        max_velocity_m_s=max_velocity_m_s,
    )

    return DomesticWaterSectionSizing(
        section_id=section.id,
        side=side,
        mode=SectionSizingMode.FORCED_INTERNAL_DIAMETER,
        demand=demand,
        selected_pipe_size=None,
        selected_pipe_size_code=None,
        theoretical_internal_diameter_mm=theoretical,
        min_required_internal_diameter_mm=min_required_diameter_mm or None,
        used_internal_diameter_mm=forced_diameter_mm,
        velocity_m_s=velocity,
        max_velocity_m_s=max_velocity_m_s,
        velocity_ok=velocity_ok,
        messages=tuple(messages),
    )


def _pipe_sizes_for_section(
    *,
    pipe_catalog: PipeCatalog,
    section: Section,
) -> Sequence[PipeSize]:
    pipe_sizes = pipe_catalog.list_sizes_for_material(section.fluid_code)
    if pipe_sizes:
        return pipe_sizes

    pipe_sizes = pipe_catalog.list_sizes_for_material(section.fluid_code.lower())
    if pipe_sizes:
        return pipe_sizes

    return list(pipe_catalog.sizes_by_code.values())


def _theoretical_internal_diameter_mm(
    *,
    demand: DomesticWaterDemand,
    pipe_sizes: Sequence[PipeSize],
    min_required_diameter_mm: float,
    max_velocity_m_s: float,
) -> float | None:
    return select_pipe_size_by_velocity(
        design_flow_l_s=demand.design_flow_l_s,
        pipe_sizes=pipe_sizes,
        max_velocity_m_s=max_velocity_m_s,
        min_internal_diameter_mm=min_required_diameter_mm or None,
    ).theoretical_internal_diameter_mm


def _append_forced_pipe_warnings(
    *,
    section: Section,
    forced_pipe_code: str,
    used_diameter_mm: float,
    velocity_m_s: float,
    velocity_ok: bool | None,
    min_required_diameter_mm: float,
    max_velocity_m_s: float,
    messages: list[EngineMessage],
) -> None:
    if (
        min_required_diameter_mm > 0.0
        and used_diameter_mm < min_required_diameter_mm
    ):
        messages.append(
            EngineMessage.warning(
                code="DOMESTIC_WATER_FORCED_PIPE_BELOW_MIN_DIAMETER",
                text=(
                    "Forced pipe internal diameter is below appliance minimum "
                    "diameter."
                ),
                context={
                    "section_id": section.id,
                    "forced_pipe_size_code": forced_pipe_code,
                    "used_internal_diameter_mm": used_diameter_mm,
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
                    "velocity_m_s": velocity_m_s,
                    "max_velocity_m_s": max_velocity_m_s,
                },
            )
        )


def _append_forced_internal_diameter_warnings(
    *,
    section: Section,
    forced_diameter_mm: float,
    velocity_m_s: float,
    velocity_ok: bool | None,
    min_required_diameter_mm: float,
    max_velocity_m_s: float,
    messages: list[EngineMessage],
) -> None:
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
                    "velocity_m_s": velocity_m_s,
                    "max_velocity_m_s": max_velocity_m_s,
                },
            )
        )