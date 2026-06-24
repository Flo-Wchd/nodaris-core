# ruff: noqa: F401
# Public barrel module: imported symbols are intentionnaly re-exported via __all__

from ndc_core.networks.domestic_water.appliance_counts import (
    apply_machine_exclusivity,
    merge_appliance_counts,
    normalize_appliance_counts,
)
from ndc_core.networks.domestic_water.appliance_propagation import (
    DomesticWaterAppliancePropagationEngine,
    DomesticWaterAppliancePropagationResult,
    propagate_cold_water_appliances,
    propagate_domestic_water_appliances,
    propagate_hot_water_appliances,
)
from ndc_core.networks.domestic_water.appliance_rules import (
    appliance_flow_for_profile,
    minimum_appliance_internal_diameter_mm,
)
from ndc_core.networks.domestic_water.demand import (
    DomesticWaterDemandBuilder,
    compute_cold_water_demand,
    compute_hot_water_demand,
)
from ndc_core.networks.domestic_water.entity_access import (
    SectionPressureLossRead,
    apply_node_pressures,
    apply_section_pressures,
    clean_entity_id,
    clean_optional_code,
    read_cell_appliance_counts,
    read_downstream_section_ids,
    read_node_local_appliance_counts,
    read_section_downstream_appliance_counts,
    read_section_pressure_loss_pa,
    write_node_downstream_appliance_counts,
    write_section_downstream_appliance_counts,
)
from ndc_core.networks.domestic_water.fluid_rules import (
    default_domestic_water_fluid_code,
    resolve_domestic_water_fluid,
)
from ndc_core.networks.domestic_water.message_binding import (
    DomesticWaterMessageBinder,
    DomesticWaterMessageBindingResult,
    bind_domestic_water_messages_to_entities,
)
from ndc_core.networks.domestic_water.network_engine import (
    DomesticWaterNetworkComputeResult,
    DomesticWaterNetworkEngine,
    DomesticWaterNetworkStep,
    DomesticWaterSectionComputeResult,
    compute_cold_water_network,
    compute_cold_water_network_from_domain,
    compute_hot_water_network,
    compute_hot_water_network_from_domain,
)
from ndc_core.networks.domestic_water.numeric import (
    positive_optional_float,
    safe_float,
    safe_non_negative_float,
    safe_positive_float,
    safe_pressure_pa,
)
from ndc_core.networks.domestic_water.pipe_rules import (
    relative_roughness_for_section,
)
from ndc_core.networks.domestic_water.pressure_loss import (
    DomesticWaterPressureLossEngine,
    compute_cold_water_section_pressure_loss,
    compute_hot_water_section_pressure_loss,
)
from ndc_core.networks.domestic_water.pressure_loss_result import (
    DomesticWaterPressureLossResult,
    build_section_pressure_loss_result,
)
from ndc_core.networks.domestic_water.pressure_loss_types import (
    DomesticWaterPressureLossMode,
)
from ndc_core.networks.domestic_water.pressure_network import (
    DomesticWaterPressureNetworkEngine,
    DomesticWaterPressurePropagationResult,
    DomesticWaterPressureSummary,
    NodePressureState,
    PressurePropagationStatus,
    TerminalPressureStatus,
    propagate_cold_water_pressures,
    propagate_hot_water_pressures,
    summarize_cold_water_worst_terminal_pressure,
    summarize_hot_water_worst_terminal_pressure,
)
from ndc_core.networks.domestic_water.profiles import (
    COLD_WATER_PROFILE,
    HOT_WATER_PROFILE,
    DomesticWaterProfile,
)
from ndc_core.networks.domestic_water.section_hydraulic_inputs import (
    DomesticWaterSectionHydraulicInputs,
    prepare_section_hydraulic_inputs,
)
from ndc_core.networks.domestic_water.section_sizing import (
    DomesticWaterSectionSizing,
    DomesticWaterSectionSizingEngine,
    SectionSizingMode,
    size_cold_water_section_from_counts,
    size_hot_water_section_from_counts,
    velocity_limit_for_context,
)
from ndc_core.networks.domestic_water.section_state import (
    apply_section_pressure_loss_state,
    apply_section_sizing_state,
)
from ndc_core.networks.domestic_water.side_matching import (
    cold_water_fluid_codes,
    domestic_water_fluid_codes_for_side,
    domestic_water_side_from_fluid_code,
    hot_water_fluid_codes,
    node_is_terminal_for_domestic_water_side,
    normalize_domestic_water_fluid_code,
    section_matches_domestic_water_side,
)
from ndc_core.networks.domestic_water.simultaneity import (
    clamp_simultaneity_factor,
    collective_dtu_simultaneity_factor,
)
from ndc_core.networks.domestic_water.singular_loss_rules import (
    collect_section_singular_zeta_values,
    zeta_from_catalog_singular_loss,
    zeta_from_section_singular_loss_item,
)
from ndc_core.networks.domestic_water.types import (
    ApplianceDemandItem,
    DomesticWaterDemand,
    DomesticWaterMethod,
    DomesticWaterSide,
)

_DOMAIN_EXPORTS = [
    "ApplianceDemandItem",
    "DomesticWaterDemand",
    "DomesticWaterDemandBuilder",
    "DomesticWaterMethod",
    "DomesticWaterProfile",
    "DomesticWaterSide",
    "COLD_WATER_PROFILE",
    "HOT_WATER_PROFILE",
]

_DEMAND_EXPORTS = [
    "compute_cold_water_demand",
    "compute_hot_water_demand",
    "appliance_flow_for_profile",
    "minimum_appliance_internal_diameter_mm",
    "clamp_simultaneity_factor",
    "collective_dtu_simultaneity_factor",
]

_APPLIANCE_PROPAGATION_EXPORTS = [
    "DomesticWaterAppliancePropagationEngine",
    "DomesticWaterAppliancePropagationResult",
    "propagate_cold_water_appliances",
    "propagate_domestic_water_appliances",
    "propagate_hot_water_appliances",
]

_NETWORK_ENGINE_EXPORTS = [
    "DomesticWaterNetworkComputeResult",
    "DomesticWaterNetworkEngine",
    "DomesticWaterNetworkStep",
    "DomesticWaterSectionComputeResult",
    "compute_cold_water_network",
    "compute_cold_water_network_from_domain",
    "compute_hot_water_network",
    "compute_hot_water_network_from_domain",
]

_PRESSURE_LOSS_EXPORTS = [
    "DomesticWaterPressureLossEngine",
    "DomesticWaterPressureLossMode",
    "DomesticWaterPressureLossResult",
    "DomesticWaterSectionHydraulicInputs",
    "build_section_pressure_loss_result",
    "compute_cold_water_section_pressure_loss",
    "compute_hot_water_section_pressure_loss",
    "prepare_section_hydraulic_inputs",
]

_PRESSURE_NETWORK_EXPORTS = [
    "DomesticWaterPressureNetworkEngine",
    "DomesticWaterPressurePropagationResult",
    "DomesticWaterPressureSummary",
    "NodePressureState",
    "PressurePropagationStatus",
    "TerminalPressureStatus",
    "propagate_cold_water_pressures",
    "propagate_hot_water_pressures",
    "summarize_cold_water_worst_terminal_pressure",
    "summarize_hot_water_worst_terminal_pressure",
]

_SECTION_SIZING_EXPORTS = [
    "DomesticWaterSectionSizing",
    "DomesticWaterSectionSizingEngine",
    "SectionSizingMode",
    "size_cold_water_section_from_counts",
    "size_hot_water_section_from_counts",
    "velocity_limit_for_context",
]

_MESSAGE_EXPORTS = [
    "DomesticWaterMessageBinder",
    "DomesticWaterMessageBindingResult",
    "bind_domestic_water_messages_to_entities",
]

_RULE_EXPORTS = [
    "apply_machine_exclusivity",
    "merge_appliance_counts",
    "normalize_appliance_counts",
    "cold_water_fluid_codes",
    "domestic_water_fluid_codes_for_side",
    "domestic_water_side_from_fluid_code",
    "hot_water_fluid_codes",
    "node_is_terminal_for_domestic_water_side",
    "normalize_domestic_water_fluid_code",
    "section_matches_domestic_water_side",
    "collect_section_singular_zeta_values",
    "zeta_from_catalog_singular_loss",
    "zeta_from_section_singular_loss_item",
    "relative_roughness_for_section",
    "default_domestic_water_fluid_code",
    "resolve_domestic_water_fluid",
]

_ENTITY_ACCESS_EXPORTS = [
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

_NUMERIC_EXPORTS = [
    "positive_optional_float",
    "safe_float",
    "safe_non_negative_float",
    "safe_positive_float",
    "safe_pressure_pa",
]

_SECTION_STATE_EXPORTS = [
    "apply_section_pressure_loss_state",
    "apply_section_sizing_state",
]

__all__ = [
    *_DOMAIN_EXPORTS,
    *_DEMAND_EXPORTS,
    *_APPLIANCE_PROPAGATION_EXPORTS,
    *_NETWORK_ENGINE_EXPORTS,
    *_PRESSURE_LOSS_EXPORTS,
    *_PRESSURE_NETWORK_EXPORTS,
    *_SECTION_SIZING_EXPORTS,
    *_MESSAGE_EXPORTS,
    *_RULE_EXPORTS,
    *_ENTITY_ACCESS_EXPORTS,
    *_NUMERIC_EXPORTS,
    *_SECTION_STATE_EXPORTS,
]