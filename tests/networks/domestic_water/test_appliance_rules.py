from __future__ import annotations

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.domain.appliances import Appliance
from ndc_core.networks.domestic_water.appliance_rules import (
    appliance_flow_for_profile,
    minimum_appliance_internal_diameter_mm,
)
from ndc_core.networks.domestic_water.profiles import (
    COLD_WATER_PROFILE,
    HOT_WATER_PROFILE,
)


def _catalog() -> ApplianceCatalog:
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
        }
    )


def test_appliance_flow_for_profile() -> None:
    appliance = Appliance(
        code="L",
        name="Lavabo",
        cold_water_flow_l_s=0.20,
        hot_water_flow_l_s=0.10,
    )

    assert appliance_flow_for_profile(appliance, COLD_WATER_PROFILE) == 0.20
    assert appliance_flow_for_profile(appliance, HOT_WATER_PROFILE) == 0.10


def test_appliance_flow_for_profile_clamps_negative_value() -> None:
    appliance = Appliance(
        code="X",
        name="Invalid",
        cold_water_flow_l_s=-1.0,
        hot_water_flow_l_s=0.0,
    )

    assert appliance_flow_for_profile(appliance, COLD_WATER_PROFILE) == 0.0
    assert appliance_flow_for_profile(appliance, HOT_WATER_PROFILE) == 0.0


def test_minimum_appliance_internal_diameter_mm_uses_only_profile_flow() -> None:
    result = minimum_appliance_internal_diameter_mm(
        appliance_catalog=_catalog(),
        appliance_counts={
            "L": 1,
            "D": 1,
            "WC": 1,
        },
        profile=HOT_WATER_PROFILE,
    )

    assert result == 12.0


def test_minimum_appliance_internal_diameter_mm_ignores_cold_only_for_hot_water() -> None:
    result = minimum_appliance_internal_diameter_mm(
        appliance_catalog=_catalog(),
        appliance_counts={
            "WC": 1,
        },
        profile=HOT_WATER_PROFILE,
    )

    assert result == 0.0


def test_minimum_appliance_internal_diameter_mm_ignores_unknown_and_zero_counts() -> None:
    result = minimum_appliance_internal_diameter_mm(
        appliance_catalog=_catalog(),
        appliance_counts={
            "UNKNOWN": 1,
            "L": 0,
            "D": -1,
        },
        profile=COLD_WATER_PROFILE,
    )

    assert result == 0.0