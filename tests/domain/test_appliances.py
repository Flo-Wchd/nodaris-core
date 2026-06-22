from ndc_core.domain.appliances import Appliance


def test_appliance_normalizes_code_and_name() -> None:
    appliance = Appliance(
        code=" lavabo ",
        name=" Lavabo ",
        cold_water_flow_l_s=0.2,
        hot_water_flow_l_s=0.2,
    )

    assert appliance.code == "lavabo"
    assert appliance.name == "Lavabo"


def test_appliance_negative_flows_are_clamped_to_zero() -> None:
    appliance = Appliance(
        code="invalid",
        name="Invalid",
        cold_water_flow_l_s=-1.0,
        hot_water_flow_l_s=-2.0,
    )

    assert appliance.cold_water_flow_l_s == 0.0
    assert appliance.hot_water_flow_l_s == 0.0
    assert not appliance.has_cold_water
    assert not appliance.has_hot_water


def test_appliance_water_flags() -> None:
    appliance = Appliance(
        code="shower",
        name="Douche",
        cold_water_flow_l_s=0.2,
        hot_water_flow_l_s=0.2,
    )

    assert appliance.has_cold_water
    assert appliance.has_hot_water


def test_appliance_total_reference_flow_uses_most_demanding_side() -> None:
    appliance = Appliance(
        code="bath",
        name="Baignoire",
        cold_water_flow_l_s=0.33,
        hot_water_flow_l_s=0.2,
    )

    assert appliance.total_reference_flow_l_s == 0.33