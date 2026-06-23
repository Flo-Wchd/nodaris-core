from ndc_core.networks import (
    ColdWaterNetworkEngine,
    DomesticWaterAppliancePropagationEngine,
    DomesticWaterAppliancePropagationResult,
    DomesticWaterDemand,
    DomesticWaterDemandBuilder,
    DomesticWaterMessageBinder,
    DomesticWaterMessageBindingResult,
    DomesticWaterMethod,
    DomesticWaterNetworkComputeResult,
    DomesticWaterNetworkEngine,
    DomesticWaterNetworkStep,
    DomesticWaterPressureLossEngine,
    DomesticWaterPressureLossMode,
    DomesticWaterPressureLossResult,
    DomesticWaterPressureNetworkEngine,
    DomesticWaterPressurePropagationResult,
    DomesticWaterPressureSummary,
    DomesticWaterSectionComputeResult,
    DomesticWaterSectionSizing,
    DomesticWaterSectionSizingEngine,
    DomesticWaterSide,
    HotWaterNetworkEngine,
    NodePressureState,
    PressurePropagationStatus,
    SectionSizingMode,
    TerminalPressureStatus,
    bind_domestic_water_messages_to_entities,
    compute_cold_water_network,
    compute_cold_water_network_from_domain,
    compute_cold_water_network_from_network,
    compute_hot_water_network,
    compute_hot_water_network_from_domain,
    compute_hot_water_network_from_network,
    propagate_cold_water_appliances,
    propagate_domestic_water_appliances,
    propagate_hot_water_appliances,
    cold_water_fluid_codes,
    domestic_water_fluid_codes_for_side,
    domestic_water_side_from_fluid_code,
    hot_water_fluid_codes,
    normalize_domestic_water_fluid_code,
    section_matches_domestic_water_side,
)
from ndc_core.networks.cold_water import (
    ColdWaterNetworkEngine as ColdWaterNetworkEngineFromPackage,
)
from ndc_core.networks.hot_water import (
    HotWaterNetworkEngine as HotWaterNetworkEngineFromPackage,
)


def test_networks_public_api_exports_facades() -> None:
    assert ColdWaterNetworkEngine is ColdWaterNetworkEngineFromPackage
    assert HotWaterNetworkEngine is HotWaterNetworkEngineFromPackage
    assert callable(compute_cold_water_network)
    assert callable(compute_cold_water_network_from_network)
    assert callable(compute_cold_water_network_from_domain)
    assert callable(compute_hot_water_network)
    assert callable(compute_hot_water_network_from_network)
    assert callable(compute_hot_water_network_from_domain)


def test_networks_public_api_exports_domestic_water_engine_types() -> None:
    assert DomesticWaterNetworkEngine is not None
    assert DomesticWaterNetworkComputeResult is not None
    assert DomesticWaterSectionComputeResult is not None
    assert DomesticWaterNetworkStep.SIZING.value == "sizing"


def test_networks_public_api_exports_domestic_water_domain_types() -> None:
    assert DomesticWaterDemand is not None
    assert DomesticWaterDemandBuilder is not None
    assert DomesticWaterMethod.COLLECTIVE_DTU.value == "collective_dtu"
    assert DomesticWaterSide.COLD_WATER.value == "cold_water"
    assert DomesticWaterSide.HOT_WATER.value == "hot_water"


def test_networks_public_api_exports_section_sizing_types() -> None:
    assert DomesticWaterSectionSizing is not None
    assert DomesticWaterSectionSizingEngine is not None
    assert SectionSizingMode.AUTOMATIC.value == "automatic"


def test_networks_public_api_exports_pressure_loss_types() -> None:
    assert DomesticWaterPressureLossEngine is not None
    assert DomesticWaterPressureLossResult is not None
    assert DomesticWaterPressureLossMode.FULL.value == "full"


def test_networks_public_api_exports_pressure_network_types() -> None:
    assert DomesticWaterPressureNetworkEngine is not None
    assert DomesticWaterPressurePropagationResult is not None
    assert DomesticWaterPressureSummary is not None
    assert NodePressureState is not None
    assert TerminalPressureStatus is not None
    assert PressurePropagationStatus.SUCCESS.value == "success"


def test_networks_public_api_exports_appliance_propagation_types() -> None:
    assert DomesticWaterAppliancePropagationEngine is not None
    assert DomesticWaterAppliancePropagationResult is not None
    assert callable(propagate_domestic_water_appliances)
    assert callable(propagate_cold_water_appliances)
    assert callable(propagate_hot_water_appliances)


def test_networks_public_api_exports_message_binding_tools() -> None:
    assert DomesticWaterMessageBinder is not None
    assert DomesticWaterMessageBindingResult is not None
    assert callable(bind_domestic_water_messages_to_entities)


def test_networks_public_api_exports_domestic_water_side_matching_tools() -> None:
    assert callable(cold_water_fluid_codes)
    assert callable(hot_water_fluid_codes)
    assert callable(domestic_water_fluid_codes_for_side)
    assert callable(domestic_water_side_from_fluid_code)
    assert callable(normalize_domestic_water_fluid_code)
    assert callable(section_matches_domestic_water_side)