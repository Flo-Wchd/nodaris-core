from math import isclose, sqrt

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.domain.appliances import Appliance
from ndc_core.networks.domestic_water.demand import (
    DomesticWaterDemandBuilder,
    compute_cold_water_demand,
    compute_hot_water_demand,
)
from ndc_core.networks.domestic_water.types import (
    DomesticWaterMethod,
    DomesticWaterSide,
)


def _catalog() -> ApplianceCatalog:
    return ApplianceCatalog(
        appliances_by_code={
            "L": Appliance(
                code="L",
                name="Lavabo",
                cold_water_flow_l_s=0.20,
                hot_water_flow_l_s=0.20,
            ),
            "D": Appliance(
                code="D",
                name="Douche",
                cold_water_flow_l_s=0.20,
                hot_water_flow_l_s=0.20,
            ),
            "WC": Appliance(
                code="WC",
                name="WC réservoir",
                cold_water_flow_l_s=0.12,
                hot_water_flow_l_s=0.0,
            ),
            "LL": Appliance(
                code="LL",
                name="Lave-linge",
                cold_water_flow_l_s=0.20,
                hot_water_flow_l_s=0.0,
            ),
            "LV": Appliance(
                code="LV",
                name="Lave-vaisselle",
                cold_water_flow_l_s=0.10,
                hot_water_flow_l_s=0.0,
            ),
        }
    )


def test_compute_cold_water_demand_raw_below_threshold() -> None:
    result = compute_cold_water_demand(
        _catalog(),
        {
            "L": 1,
            "D": 1,
            "WC": 1,
        },
    )

    assert result.ok
    assert result.value is not None

    demand = result.value

    assert demand.side is DomesticWaterSide.COLD_WATER
    assert demand.method is DomesticWaterMethod.COLLECTIVE_DTU
    assert demand.declared_appliance_count == 3
    assert demand.effective_appliance_count == 3
    assert demand.raw_flow_l_s == 0.52
    assert demand.simultaneity_factor == 1.0
    assert demand.design_flow_l_s == 0.52
    assert demand.has_flow


def test_compute_cold_water_demand_with_collective_simultaneity() -> None:
    result = compute_cold_water_demand(
        _catalog(),
        {
            "L": 3,
            "D": 2,
            "WC": 1,
        },
    )

    assert result.value is not None

    demand = result.value
    expected_factor = 0.8 / sqrt(6 - 1)

    assert demand.declared_appliance_count == 6
    assert demand.effective_appliance_count == 6
    assert isclose(demand.raw_flow_l_s, 1.12)
    assert isclose(demand.simultaneity_factor, expected_factor)
    assert isclose(demand.design_flow_l_s, 1.12 * expected_factor)


def test_compute_hot_water_demand_ignores_cold_only_appliances() -> None:
    result = compute_hot_water_demand(
        _catalog(),
        {
            "L": 1,
            "WC": 1,
        },
    )

    assert result.ok
    assert result.value is not None

    demand = result.value

    assert demand.side is DomesticWaterSide.HOT_WATER
    assert demand.declared_appliance_count == 2
    assert demand.effective_appliance_count == 2
    assert demand.raw_flow_l_s == 0.20
    assert demand.design_flow_l_s == 0.20
    assert any(
        message.code == "DOMESTIC_WATER_APPLIANCE_IGNORED_FOR_SIDE"
        for message in demand.messages
    )


def test_unknown_appliance_creates_warning_without_failure() -> None:
    result = compute_cold_water_demand(
        _catalog(),
        {
            "UNKNOWN": 1,
            "L": 1,
        },
    )

    assert result.ok
    assert result.value is not None
    assert result.value.raw_flow_l_s == 0.20
    assert result.value.has_warnings
    assert any(
        message.code == "DOMESTIC_WATER_UNKNOWN_APPLIANCE"
        for message in result.value.messages
    )


def test_machine_exclusivity_counts_ll_lv_as_one_effective_machine() -> None:
    result = compute_cold_water_demand(
        _catalog(),
        {
            "LL": 1,
            "LV": 1,
            "L": 1,
        },
    )

    assert result.ok
    assert result.value is not None

    demand = result.value

    assert demand.declared_appliance_count == 3
    assert demand.effective_appliance_count == 2
    assert isclose(demand.raw_flow_l_s, 0.40)
    assert any(
        message.code == "DOMESTIC_WATER_MACHINE_EXCLUSIVITY_APPLIED"
        for message in demand.messages
    )

    machine_items = [
        item
        for item in demand.items
        if item.appliance_code in {"LL", "LV"}
    ]

    assert len(machine_items) == 1
    assert machine_items[0].declared_count == 1
    assert machine_items[0].effective_count == 1


def test_demand_builder_accepts_lowercase_catalog_lookup() -> None:
    result = DomesticWaterDemandBuilder.cold_water(_catalog()).compute_from_counts(
        {"l": 1}
    )

    assert result.ok
    assert result.value is not None
    assert result.value.raw_flow_l_s == 0.20


def test_invalid_counts_are_ignored() -> None:
    result = compute_cold_water_demand(
        _catalog(),
        {
            "L": 1,
            "D": 0,
            "WC": -1,
        },
    )

    assert result.value is not None
    assert result.value.declared_appliance_count == 1
    assert result.value.raw_flow_l_s == 0.20