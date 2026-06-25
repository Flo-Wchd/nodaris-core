from __future__ import annotations

from ndc_core.common.result import Result
from ndc_core.domain.networks.section import Section
from ndc_core.networks.domestic_water.section_sizing_context import (
    DomesticWaterSectionSizingContext,
)
from ndc_core.networks.domestic_water.section_sizing_result import (
    DomesticWaterSectionSizing,
)
from ndc_core.networks.domestic_water.section_state import (
    apply_section_sizing_state,
)


def finalize_section_sizing_result(
    *,
    section: Section,
    context: DomesticWaterSectionSizingContext,
    sizing: DomesticWaterSectionSizing,
) -> Result[DomesticWaterSectionSizing]:
    """
    Apply sizing outputs to the section and wrap the engine result.

    This is the finalization point for a section sizing computation:
    - write calculated state back to the Section;
    - preserve managed messages;
    - choose the Result status from the sizing content.
    """

    apply_section_sizing_state(
        section=section,
        sizing=sizing,
        raw_counts=context.raw_appliance_counts,
        effective_counts=context.effective_appliance_counts,
    )

    if sizing.has_errors:
        return Result.failure(value=sizing, messages=context.messages)

    if sizing.has_warnings:
        return Result.partial(value=sizing, messages=context.messages)

    return Result.success(value=sizing, messages=context.messages)