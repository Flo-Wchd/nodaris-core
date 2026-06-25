from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import SectionUsageContext
from ndc_core.networks.domestic_water.appliance_counts import (
    normalize_appliance_counts,
)
from ndc_core.networks.domestic_water.appliance_rules import (
    minimum_appliance_internal_diameter_mm,
)
from ndc_core.networks.domestic_water.demand import DomesticWaterDemandBuilder
from ndc_core.networks.domestic_water.profiles import DomesticWaterProfile
from ndc_core.networks.domestic_water.types import DomesticWaterDemand


@dataclass(slots=True)
class DomesticWaterSectionSizingContext:
    """Prepared inputs for one domestic water section sizing."""

    demand: DomesticWaterDemand
    raw_appliance_counts: dict[str, int]
    effective_appliance_counts: dict[str, int]
    min_required_diameter_mm: float
    max_velocity_m_s: float
    messages: list[EngineMessage]


def build_section_sizing_context(
    *,
    section: Section,
    appliance_counts: Mapping[str, int],
    appliance_catalog: ApplianceCatalog,
    profile: DomesticWaterProfile,
    max_velocity_m_s: float | None = None,
) -> Result[DomesticWaterSectionSizingContext]:
    """Prepare demand, counts and sizing limits for one section."""

    messages: list[EngineMessage] = []

    demand_result = DomesticWaterDemandBuilder(
        appliance_catalog=appliance_catalog,
        profile=profile,
    ).compute_from_counts(appliance_counts)

    messages.extend(demand_result.messages)

    if demand_result.value is None:
        return Result.failure(messages=messages)

    demand = demand_result.value
    raw_counts = normalize_appliance_counts(appliance_counts)
    effective_counts = {
        item.appliance_code: item.effective_count
        for item in demand.items
        if item.effective_count > 0
    }
    min_required_diameter = max(
        minimum_appliance_internal_diameter_mm(
            appliance_catalog=appliance_catalog,
            appliance_counts=raw_counts,
            profile=profile,
        ),
        0.0,
    )

    context = DomesticWaterSectionSizingContext(
        demand=demand,
        raw_appliance_counts=raw_counts,
        effective_appliance_counts=effective_counts,
        min_required_diameter_mm=min_required_diameter,
        max_velocity_m_s=max_velocity_m_s
        or velocity_limit_for_context(section.usage_context),
        messages=messages,
    )

    return Result.success(value=context, messages=messages)


def velocity_limit_for_context(
    usage_context: SectionUsageContext | str | None,
) -> float:
    """
    Return default velocity limit for domestic water.

    Current DTU-oriented defaults:
    - basement / technical room: 2.0 m/s
    - riser: 1.5 m/s
    - dwelling: 1.5 m/s
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