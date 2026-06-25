import ndc_core.networks as networks_api
import ndc_core.networks.domestic_water as domestic_water_api

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
    apply_machine_exclusivity,
    merge_appliance_counts,
    normalize_appliance_counts,
    apply_node_pressures,
    apply_section_pressures,
    clean_entity_id,
    clean_optional_code,
    read_downstream_section_ids,
    write_node_downstream_appliance_counts,
    write_section_downstream_appliance_counts,
    positive_optional_float,
    safe_float,
    safe_non_negative_float,
    safe_positive_float,
    safe_pressure_pa,
    apply_section_pressure_loss_state,
    apply_section_sizing_state,
    appliance_flow_for_profile,
    minimum_appliance_internal_diameter_mm,
    read_cell_appliance_counts,
    read_node_local_appliance_counts,
    read_section_downstream_appliance_counts,
    SectionPressureLossRead,
    node_is_terminal_for_domestic_water_side,
    read_section_pressure_loss_pa,
    collect_section_singular_zeta_values,
    zeta_from_catalog_singular_loss,
    zeta_from_section_singular_loss_item,
    relative_roughness_for_section,
    default_domestic_water_fluid_code,
    resolve_domestic_water_fluid,
    DomesticWaterSectionHydraulicInputs,
    prepare_section_hydraulic_inputs,
    build_section_pressure_loss_result,
    select_section_diameter,
    DomesticWaterNetworkDiagnostic,
    DomesticWaterNetworkDiagnosticStatus,
    build_domestic_water_network_diagnostic,
)
from ndc_core.networks.cold_water import (
    ColdWaterNetworkEngine as ColdWaterNetworkEngineFromPackage,
)
from ndc_core.networks.hot_water import (
    HotWaterNetworkEngine as HotWaterNetworkEngineFromPackage,
)
from ndc_core.networks.domestic_water.pressure_network_result import (
    DomesticWaterPressurePropagationResult as PressurePropagationResultFromModule,
    DomesticWaterPressureSummary as PressureSummaryFromModule,
    NodePressureState as NodePressureStateFromModule,
    PressurePropagationStatus as PressurePropagationStatusFromModule,
    TerminalPressureStatus as TerminalPressureStatusFromModule,
)
from ndc_core.networks.domestic_water.section_sizing_result import (
    DomesticWaterSectionSizing as SectionSizingFromModule,
    SectionSizingMode as SectionSizingModeFromModule,
)
from ndc_core.networks.domestic_water.section_diameter_selection import (
    select_section_diameter as select_section_diameter_from_module,
)
from ndc_core.networks.domestic_water.section_no_flow_sizing import (
    build_no_flow_section_sizing,
)
from ndc_core.networks.domestic_water.section_sizing_context import (
    build_section_sizing_context,
)
from ndc_core.networks.domestic_water.section_sizing_finalization import (
    finalize_section_sizing_result,
)
from ndc_core.networks.domestic_water.pressure_summary import (
    build_pressure_summary_from_propagation,
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


def test_networks_public_api_exports_domestic_water_diagnostic_types() -> None:
    assert DomesticWaterNetworkDiagnostic is not None
    assert DomesticWaterNetworkDiagnosticStatus.OK.value == "ok"
    assert callable(build_domestic_water_network_diagnostic)


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
    assert DomesticWaterSectionSizing is SectionSizingFromModule
    assert SectionSizingMode is SectionSizingModeFromModule
    assert callable(select_section_diameter)
    assert select_section_diameter is select_section_diameter_from_module


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
    assert DomesticWaterPressurePropagationResult is PressurePropagationResultFromModule
    assert DomesticWaterPressureSummary is PressureSummaryFromModule
    assert NodePressureState is NodePressureStateFromModule
    assert TerminalPressureStatus is TerminalPressureStatusFromModule
    assert PressurePropagationStatus is PressurePropagationStatusFromModule


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
    assert callable(node_is_terminal_for_domestic_water_side)


def test_networks_public_api_exports_domestic_water_appliance_count_tools() -> None:
    assert callable(normalize_appliance_counts)
    assert callable(merge_appliance_counts)
    assert callable(apply_machine_exclusivity)


def test_networks_public_api_exports_domestic_water_entity_access_tools() -> None:
    assert callable(clean_entity_id)
    assert callable(clean_optional_code)
    assert callable(read_downstream_section_ids)
    assert callable(write_section_downstream_appliance_counts)
    assert callable(write_node_downstream_appliance_counts)
    assert callable(apply_section_pressures)
    assert callable(apply_node_pressures)
    assert callable(read_cell_appliance_counts)
    assert callable(read_node_local_appliance_counts)
    assert callable(read_section_downstream_appliance_counts)
    assert SectionPressureLossRead is not None
    assert callable(read_section_pressure_loss_pa)


def test_networks_public_api_exports_domestic_water_numeric_tools() -> None:
    assert callable(safe_float)
    assert callable(safe_positive_float)
    assert callable(safe_non_negative_float)
    assert callable(safe_pressure_pa)
    assert callable(positive_optional_float)


def test_networks_public_api_exports_domestic_water_section_state_tools() -> None:
    assert callable(apply_section_sizing_state)
    assert callable(apply_section_pressure_loss_state)


def test_networks_public_api_exports_domestic_water_appliance_rules_tools() -> None:
    assert callable(appliance_flow_for_profile)
    assert callable(minimum_appliance_internal_diameter_mm)


def test_networks_public_api_exports_domestic_water_singular_loss_rules() -> None:
    assert callable(collect_section_singular_zeta_values)
    assert callable(zeta_from_catalog_singular_loss)
    assert callable(zeta_from_section_singular_loss_item)


def test_networks_public_api_exports_domestic_water_pipe_rules() -> None:
    assert callable(relative_roughness_for_section)


def test_networks_public_api_exports_domestic_water_fluid_rules() -> None:
    assert callable(default_domestic_water_fluid_code)
    assert callable(resolve_domestic_water_fluid)


def test_networks_public_api_exports_domestic_water_section_hydraulic_inputs() -> None:
    assert DomesticWaterSectionHydraulicInputs is not None
    assert callable(prepare_section_hydraulic_inputs)


def test_networks_public_api_exports_domestic_water_pressure_loss_result_tools() -> None:
    assert callable(build_section_pressure_loss_result)


def test_networks_public_api_all_is_unique_and_resolvable() -> None:
    assert len(networks_api.__all__) == len(set(networks_api.__all__))

    for exported_name in networks_api.__all__:
        assert hasattr(networks_api, exported_name)


def test_domestic_water_public_api_all_is_unique_and_resolvable() -> None:
    assert len(domestic_water_api.__all__) == len(set(domestic_water_api.__all__))

    for exported_name in domestic_water_api.__all__:
        assert hasattr(domestic_water_api, exported_name)


def test_no_flow_section_sizing_helper_stays_internal() -> None:
    assert build_no_flow_section_sizing is not None
    assert "build_no_flow_section_sizing" not in domestic_water_api.__all__


def test_networks_public_api_does_not_export_no_flow_helper() -> None:
    assert "build_no_flow_section_sizing" not in networks_api.__all__


def test_section_sizing_context_helper_stays_internal() -> None:
    assert build_section_sizing_context is not None
    assert "build_section_sizing_context" not in domestic_water_api.__all__


def test_networks_public_api_does_not_export_section_sizing_context_helper() -> None:
    assert "build_section_sizing_context" not in networks_api.__all__


def test_section_sizing_finalization_helper_stays_internal() -> None:
    assert finalize_section_sizing_result is not None
    assert "finalize_section_sizing_result" not in domestic_water_api.__all__


def test_networks_public_api_does_not_export_section_sizing_finalization_helper() -> None:
    assert "finalize_section_sizing_result" not in networks_api.__all__


def test_pressure_summary_builder_stays_internal() -> None:
    assert build_pressure_summary_from_propagation is not None
    assert "build_pressure_summary_from_propagation" not in domestic_water_api.__all__


def test_networks_public_api_does_not_export_pressure_summary_builder() -> None:
    assert "build_pressure_summary_from_propagation" not in networks_api.__all__