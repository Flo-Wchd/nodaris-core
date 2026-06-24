# ruff: noqa: F401
# Public barrel module: imported symbols are intentionnaly re-exported via __all__

from ndc_core.networks.cold_water import (
    ColdWaterNetworkEngine,
    compute_cold_water_network,
    compute_cold_water_network_from_network,
)
from ndc_core.networks.domestic_water import (
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
    DomesticWaterSectionHydraulicInputs,
    DomesticWaterSectionSizing,
    DomesticWaterSectionSizingEngine,
    DomesticWaterSide,
    NodePressureState,
    PressurePropagationStatus,
    SectionPressureLossRead,
    SectionSizingMode,
    TerminalPressureStatus,
    appliance_flow_for_profile,
    apply_machine_exclusivity,
    apply_node_pressures,
    apply_section_pressure_loss_state,
    apply_section_pressures,
    apply_section_sizing_state,
    bind_domestic_water_messages_to_entities,
    build_section_pressure_loss_result,
    clean_entity_id,
    clean_optional_code,
    cold_water_fluid_codes,
    collect_section_singular_zeta_values,
    compute_cold_water_network_from_domain,
    compute_hot_water_network_from_domain,
    default_domestic_water_fluid_code,
    domestic_water_fluid_codes_for_side,
    domestic_water_side_from_fluid_code,
    hot_water_fluid_codes,
    merge_appliance_counts,
    minimum_appliance_internal_diameter_mm,
    node_is_terminal_for_domestic_water_side,
    normalize_appliance_counts,
    normalize_domestic_water_fluid_code,
    positive_optional_float,
    prepare_section_hydraulic_inputs,
    propagate_cold_water_appliances,
    propagate_domestic_water_appliances,
    propagate_hot_water_appliances,
    read_cell_appliance_counts,
    read_downstream_section_ids,
    read_node_local_appliance_counts,
    read_section_downstream_appliance_counts,
    read_section_pressure_loss_pa,
    relative_roughness_for_section,
    resolve_domestic_water_fluid,
    safe_float,
    safe_non_negative_float,
    safe_positive_float,
    safe_pressure_pa,
    section_matches_domestic_water_side,
    write_node_downstream_appliance_counts,
    write_section_downstream_appliance_counts,
    zeta_from_catalog_singular_loss,
    zeta_from_section_singular_loss_item,
    select_section_diameter,
)
from ndc_core.networks.hot_water import (
    HotWaterNetworkEngine,
    compute_hot_water_network,
    compute_hot_water_network_from_network,
)

_FACADE_EXPORTS = [
    "ColdWaterNetworkEngine",
    "HotWaterNetworkEngine",
    "compute_cold_water_network",
    "compute_cold_water_network_from_network",
    "compute_cold_water_network_from_domain",
    "compute_hot_water_network",
    "compute_hot_water_network_from_network",
    "compute_hot_water_network_from_domain",
]

_DOMESTIC_WATER_DOMAIN_EXPORTS = [
    "DomesticWaterDemand",
    "DomesticWaterDemandBuilder",
    "DomesticWaterMethod",
    "DomesticWaterSide",
]

_DOMESTIC_WATER_ENGINE_EXPORTS = [
    "DomesticWaterNetworkComputeResult",
    "DomesticWaterNetworkEngine",
    "DomesticWaterNetworkStep",
    "DomesticWaterSectionComputeResult",
]

_DOMESTIC_WATER_PRESSURE_EXPORTS = [
    "DomesticWaterPressureLossEngine",
    "DomesticWaterPressureLossMode",
    "DomesticWaterPressureLossResult",
    "DomesticWaterPressureNetworkEngine",
    "DomesticWaterPressurePropagationResult",
    "DomesticWaterPressureSummary",
    "DomesticWaterSectionHydraulicInputs",
    "NodePressureState",
    "PressurePropagationStatus",
    "TerminalPressureStatus",
    "build_section_pressure_loss_result",
    "prepare_section_hydraulic_inputs",
]

_DOMESTIC_WATER_SIZING_EXPORTS = [
    "DomesticWaterSectionSizing",
    "DomesticWaterSectionSizingEngine",
    "SectionSizingMode",
    "select_section_diameter",
]

_DOMESTIC_WATER_APPLIANCE_EXPORTS = [
    "DomesticWaterAppliancePropagationEngine",
    "DomesticWaterAppliancePropagationResult",
    "appliance_flow_for_profile",
    "apply_machine_exclusivity",
    "merge_appliance_counts",
    "minimum_appliance_internal_diameter_mm",
    "normalize_appliance_counts",
    "propagate_cold_water_appliances",
    "propagate_domestic_water_appliances",
    "propagate_hot_water_appliances",
]

_DOMESTIC_WATER_MESSAGE_EXPORTS = [
    "DomesticWaterMessageBinder",
    "DomesticWaterMessageBindingResult",
    "bind_domestic_water_messages_to_entities",
]

_DOMESTIC_WATER_RULE_EXPORTS = [
    "cold_water_fluid_codes",
    "collect_section_singular_zeta_values",
    "default_domestic_water_fluid_code",
    "domestic_water_fluid_codes_for_side",
    "domestic_water_side_from_fluid_code",
    "hot_water_fluid_codes",
    "node_is_terminal_for_domestic_water_side",
    "normalize_domestic_water_fluid_code",
    "relative_roughness_for_section",
    "resolve_domestic_water_fluid",
    "section_matches_domestic_water_side",
    "zeta_from_catalog_singular_loss",
    "zeta_from_section_singular_loss_item",
]

_DOMESTIC_WATER_ENTITY_ACCESS_EXPORTS = [
    "SectionPressureLossRead",
    "apply_node_pressures",
    "apply_section_pressures",
    "clean_entity_id",
    "clean_optional_code",
    "read_cell_appliance_counts",
    "read_downstream_section_ids",
    "read_node_local_appliance_counts",
    "read_section_downstream_appliance_counts",
    "read_section_pressure_loss_pa",
    "write_node_downstream_appliance_counts",
    "write_section_downstream_appliance_counts",
]

_DOMESTIC_WATER_NUMERIC_EXPORTS = [
    "positive_optional_float",
    "safe_float",
    "safe_non_negative_float",
    "safe_positive_float",
    "safe_pressure_pa",
]

_DOMESTIC_WATER_SECTION_STATE_EXPORTS = [
    "apply_section_pressure_loss_state",
    "apply_section_sizing_state",
]

__all__ = [
    *_FACADE_EXPORTS,
    *_DOMESTIC_WATER_DOMAIN_EXPORTS,
    *_DOMESTIC_WATER_ENGINE_EXPORTS,
    *_DOMESTIC_WATER_PRESSURE_EXPORTS,
    *_DOMESTIC_WATER_SIZING_EXPORTS,
    *_DOMESTIC_WATER_APPLIANCE_EXPORTS,
    *_DOMESTIC_WATER_MESSAGE_EXPORTS,
    *_DOMESTIC_WATER_RULE_EXPORTS,
    *_DOMESTIC_WATER_ENTITY_ACCESS_EXPORTS,
    *_DOMESTIC_WATER_NUMERIC_EXPORTS,
    *_DOMESTIC_WATER_SECTION_STATE_EXPORTS,
]