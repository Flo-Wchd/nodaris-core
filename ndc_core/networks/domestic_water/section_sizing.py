from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.common.result import Result
from ndc_core.domain.networks.section import Section
from ndc_core.networks.domestic_water.profiles import (
    COLD_WATER_PROFILE,
    HOT_WATER_PROFILE,
    DomesticWaterProfile,
)
from ndc_core.networks.domestic_water.section_diameter_selection import (
    select_section_diameter,
)
from ndc_core.networks.domestic_water.section_no_flow_sizing import (
    build_no_flow_section_sizing,
)
from ndc_core.networks.domestic_water.section_sizing_context import (
    build_section_sizing_context,
    velocity_limit_for_context,
)
from ndc_core.networks.domestic_water.section_sizing_result import (
    DomesticWaterSectionSizing,
    SectionSizingMode,
)
from ndc_core.networks.domestic_water.section_sizing_finalization import (
    finalize_section_sizing_result,
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
        context_result = build_section_sizing_context(
            section=section,
            appliance_counts=appliance_counts,
            appliance_catalog=self.appliance_catalog,
            profile=self.profile,
            max_velocity_m_s=max_velocity_m_s,
        )

        if context_result.value is None:
            return Result.failure(messages=context_result.messages)

        context = context_result.value

        if context.demand.design_flow_l_s <= 0.0:
            sizing = build_no_flow_section_sizing(
                section=section,
                demand=context.demand,
                side=self.profile.side,
                min_required_diameter_mm=context.min_required_diameter_mm,
                max_velocity_m_s=context.max_velocity_m_s,
                messages=context.messages,
            )
            return finalize_section_sizing_result(
                section=section,
                context=context,
                sizing=sizing,
            )

        sizing = select_section_diameter(
            section=section,
            demand=context.demand,
            pipe_catalog=self.pipe_catalog,
            side=self.profile.side,
            min_required_diameter_mm=context.min_required_diameter_mm,
            max_velocity_m_s=context.max_velocity_m_s,
            messages=context.messages,
        )

        return finalize_section_sizing_result(
            section=section,
            context=context,
            sizing=sizing,
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


__all__ = [
    "DomesticWaterSectionSizing",
    "DomesticWaterSectionSizingEngine",
    "SectionSizingMode",
    "size_cold_water_section_from_counts",
    "size_hot_water_section_from_counts",
    "velocity_limit_for_context",
]