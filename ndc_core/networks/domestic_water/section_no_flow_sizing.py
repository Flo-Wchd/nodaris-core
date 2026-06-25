from __future__ import annotations

from ndc_core.common.messages import EngineMessage
from ndc_core.domain.networks.section import Section
from ndc_core.networks.domestic_water.section_sizing_result import (
    DomesticWaterSectionSizing,
    SectionSizingMode,
)
from ndc_core.networks.domestic_water.types import (
    DomesticWaterDemand,
    DomesticWaterSide,
)


def build_no_flow_section_sizing(
    *,
    section: Section,
    demand: DomesticWaterDemand,
    side: DomesticWaterSide,
    min_required_diameter_mm: float,
    max_velocity_m_s: float,
    messages: list[EngineMessage],
) -> DomesticWaterSectionSizing:
    """
    Build a managed sizing result for a section with zero design flow.

    This keeps the no-flow case explicit without raising an exception:
    the section demand is known, but no diameter can be selected because
    there is no hydraulic flow to size.
    """

    messages.append(
        EngineMessage.warning(
            code="DOMESTIC_WATER_SECTION_NO_FLOW",
            text="Section demand is zero; diameter sizing was not performed.",
            context={"section_id": section.id},
        )
    )

    return DomesticWaterSectionSizing(
        section_id=section.id,
        side=side,
        mode=SectionSizingMode.AUTOMATIC,
        demand=demand,
        selected_pipe_size=None,
        selected_pipe_size_code=None,
        theoretical_internal_diameter_mm=None,
        min_required_internal_diameter_mm=min_required_diameter_mm or None,
        used_internal_diameter_mm=None,
        velocity_m_s=None,
        max_velocity_m_s=max_velocity_m_s,
        velocity_ok=None,
        messages=tuple(messages),
    )