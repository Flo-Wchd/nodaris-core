from __future__ import annotations

from ndc_core.networks import ColdWaterNetworkEngine, compute_cold_water_network_from_network
from ndc_core.networks.domestic_water.types import DomesticWaterSide
from tests.helpers.catalog_builders import (
    domestic_water_appliance_catalog,
    domestic_water_fluid_catalog,
    domestic_water_pipe_catalog,
    domestic_water_singular_loss_catalog,
)
from tests.helpers.network_builders import domestic_water_branching_network
from ndc_core.networks.domestic_water.pressure_network_result import (
    PressureSummaryStatus,
)


def test_cold_water_full_workflow_on_branching_network() -> None:
    network = domestic_water_branching_network()

    result = ColdWaterNetworkEngine.from_network(
        network=network,
        appliance_catalog=domestic_water_appliance_catalog(),
        pipe_catalog=domestic_water_pipe_catalog(),
        fluid_catalog=domestic_water_fluid_catalog(),
        singular_loss_catalog=domestic_water_singular_loss_catalog(),
    ).compute_all(
        source_node_id="N0",
        source_pressure_bar=3.0,
        min_required_pressure_bar=1.0,
    )

    assert result.ok
    assert result.value is not None

    compute = result.value

    assert compute.side is DomesticWaterSide.COLD_WATER
    assert set(compute.section_results) == {
        "S_EFS_MAIN",
        "S_EFS_A",
        "S_EFS_B",
    }
    assert compute.section_count == 3
    assert compute.sized_section_count == 3
    assert compute.pressure_loss_section_count == 3
    assert compute.has_pressure_propagation
    assert compute.has_pressure_summary

    assert compute.pressure_propagation is not None
    assert set(compute.pressure_propagation.reached_node_ids) == {
        "N0",
        "N_EFS_SPLIT",
        "N_EFS_A",
        "N_EFS_B",
    }

    assert compute.pressure_summary is not None
    assert compute.pressure_summary.has_worst_terminal
    assert compute.pressure_summary.worst_terminal is not None
    assert compute.pressure_summary.propagation is compute.pressure_propagation
    assert compute.pressure_summary.status is PressureSummaryStatus.OK
    assert compute.pressure_summary.is_ok
    assert compute.pressure_summary.terminal_count == 2
    assert compute.pressure_summary.critical_node_id in {
        "N_EFS_A",
        "N_EFS_B",
    }
    assert compute.pressure_summary.pressure_margin_bar is not None
    assert compute.pressure_summary.worst_terminal.node_id in {
        "N_EFS_A",
        "N_EFS_B",
    }

    main = network.get_section("S_EFS_MAIN")
    branch_a = network.get_section("S_EFS_A")
    branch_b = network.get_section("S_EFS_B")
    hot_main = network.get_section("S_ECS_MAIN")

    assert main.downstream_appliance_counts == {
        "L": 2,
        "D": 1,
        "WC": 2,
        "E": 1,
        "LL": 1,
        "LV": 1,
    }
    assert branch_a.downstream_appliance_counts == {
        "L": 1,
        "D": 1,
        "WC": 1,
    }
    assert branch_b.downstream_appliance_counts == {
        "L": 1,
        "E": 1,
        "WC": 1,
        "LL": 1,
        "LV": 1,
    }

    assert main.selected_pipe_size_code == "EFS26"
    assert main.selected_internal_diameter_mm == 26.0
    assert branch_a.selected_internal_diameter_mm is not None
    assert branch_b.selected_internal_diameter_mm is not None

    assert main.total_pressure_loss_pa is not None
    assert branch_a.total_pressure_loss_pa is not None
    assert branch_b.total_pressure_loss_pa is not None

    assert main.pressure_start_pa == 300_000.0
    assert main.pressure_end_pa is not None
    assert branch_a.pressure_start_pa == main.pressure_end_pa
    assert branch_b.pressure_start_pa == main.pressure_end_pa
    assert branch_a.pressure_end_pa is not None
    assert branch_b.pressure_end_pa is not None

    assert hot_main.downstream_appliance_counts == {}
    assert hot_main.selected_internal_diameter_mm is None
    assert hot_main.total_pressure_loss_pa is None
    assert hot_main.pressure_start_pa is None
    assert hot_main.pressure_end_pa is None


def test_cold_water_functional_entry_point_full_workflow() -> None:
    network = domestic_water_branching_network()

    result = compute_cold_water_network_from_network(
        network=network,
        appliance_catalog=domestic_water_appliance_catalog(),
        pipe_catalog=domestic_water_pipe_catalog(),
        fluid_catalog=domestic_water_fluid_catalog(),
        singular_loss_catalog=domestic_water_singular_loss_catalog(),
        source_node_id="N0",
        source_pressure_bar=3.0,
        min_required_pressure_bar=1.0,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.side is DomesticWaterSide.COLD_WATER
    assert result.value.pressure_summary is not None
    assert result.value.pressure_summary.has_worst_terminal