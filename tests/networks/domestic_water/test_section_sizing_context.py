from __future__ import annotations

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.domain.appliances import Appliance
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import SectionUsageContext
from ndc_core.networks.domestic_water.profiles import (
    COLD_WATER_PROFILE,
    HOT_WATER_PROFILE,
)
from ndc_core.networks.domestic_water.section_sizing import (
    velocity_limit_for_context as sizing_velocity_limit_for_context,
)
from ndc_core.networks.domestic_water.section_sizing_context import (
    DomesticWaterSectionSizingContext,
    build_section_sizing_context,
    velocity_limit_for_context,
)


def _appliance_catalog() -> ApplianceCatalog:
    return ApplianceCatalog(
        appliances_by_code={
            "L": Appliance(
                code="L",
                name="Lavabo",
                cold_water_flow_l_s=0.20,
                hot_water_flow_l_s=0.20,
                min_internal_diameter_mm=10.0,
            ),
            "D": Appliance(
                code="D",
                name="Douche",
                cold_water_flow_l_s=0.20,
                hot_water_flow_l_s=0.20,
                min_internal_diameter_mm=12.0,
            ),
            "WC": Appliance(
                code="WC",
                name="WC",
                cold_water_flow_l_s=0.12,
                hot_water_flow_l_s=0.0,
                min_internal_diameter_mm=10.0,
            ),
            "LL": Appliance(
                code="LL",
                name="Lave-linge",
                cold_water_flow_l_s=0.20,
                hot_water_flow_l_s=0.0,
                min_internal_diameter_mm=10.0,
            ),
            "LV": Appliance(
                code="LV",
                name="Lave-vaisselle",
                cold_water_flow_l_s=0.10,
                hot_water_flow_l_s=0.0,
                min_internal_diameter_mm=10.0,
            ),
        }
    )


def _section(**kwargs: object) -> Section:
    values = {
        "id": "S1",
        "name": "Section 1",
        "upstream_node_id": "N1",
        "downstream_node_id": "N2",
        "fluid_code": "EFS",
        "usage_context": SectionUsageContext.RISER,
        "length_m": 10.0,
    }
    values.update(kwargs)
    return Section(**values)


def test_build_section_sizing_context_for_cold_water() -> None:
    result = build_section_sizing_context(
        section=_section(),
        appliance_counts={"L": 1, "D": 1, "WC": 1},
        appliance_catalog=_appliance_catalog(),
        profile=COLD_WATER_PROFILE,
    )

    assert result.ok
    assert isinstance(result.value, DomesticWaterSectionSizingContext)

    context = result.value

    assert context.demand.design_flow_l_s == 0.52
    assert context.raw_appliance_counts == {"L": 1, "D": 1, "WC": 1}
    assert context.effective_appliance_counts == {"L": 1, "D": 1, "WC": 1}
    assert context.min_required_diameter_mm == 12.0
    assert context.max_velocity_m_s == 1.5
    assert context.messages == list(result.messages)


def test_build_section_sizing_context_respects_machine_exclusivity() -> None:
    result = build_section_sizing_context(
        section=_section(),
        appliance_counts={"LL": 1, "LV": 1, "L": 1},
        appliance_catalog=_appliance_catalog(),
        profile=COLD_WATER_PROFILE,
    )

    assert result.ok
    assert result.value is not None

    context = result.value

    assert context.demand.declared_appliance_count == 3
    assert context.demand.effective_appliance_count == 2
    assert context.raw_appliance_counts == {"LL": 1, "LV": 1, "L": 1}
    assert context.effective_appliance_counts in (
        {"LL": 1, "L": 1},
        {"LV": 1, "L": 1},
    )


def test_build_section_sizing_context_keeps_zero_hot_water_demand() -> None:
    result = build_section_sizing_context(
        section=_section(fluid_code="ECS"),
        appliance_counts={"WC": 1},
        appliance_catalog=_appliance_catalog(),
        profile=HOT_WATER_PROFILE,
    )

    assert result.ok
    assert result.value is not None

    context = result.value

    assert context.demand.design_flow_l_s == 0.0
    assert context.raw_appliance_counts == {"WC": 1}
    assert context.effective_appliance_counts == {}
    assert context.min_required_diameter_mm == 0.0


def test_build_section_sizing_context_accepts_manual_velocity_limit() -> None:
    result = build_section_sizing_context(
        section=_section(),
        appliance_counts={"L": 1},
        appliance_catalog=_appliance_catalog(),
        profile=COLD_WATER_PROFILE,
        max_velocity_m_s=1.2,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.max_velocity_m_s == 1.2


def test_velocity_limit_for_context_is_kept_compatible_from_section_sizing() -> None:
    assert velocity_limit_for_context(SectionUsageContext.RISER) == 1.5
    assert velocity_limit_for_context(SectionUsageContext.DWELLING) == 1.5
    assert velocity_limit_for_context(SectionUsageContext.BASEMENT) == 2.0
    assert velocity_limit_for_context(None) == 2.0

    assert sizing_velocity_limit_for_context is velocity_limit_for_context