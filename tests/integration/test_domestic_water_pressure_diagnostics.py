from __future__ import annotations

from ndc_core.networks import ColdWaterNetworkEngine, HotWaterNetworkEngine
from ndc_core.networks.domestic_water.pressure_network_result import (
    PressureSummaryStatus,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide
from tests.helpers.catalog_builders import (
    domestic_water_appliance_catalog,
    domestic_water_fluid_catalog,
    domestic_water_pipe_catalog,
    domestic_water_singular_loss_catalog,
)
from tests.helpers.network_builders import domestic_water_branching_network


def test_cold_water_pressure_diagnostic_ok_on_reference_network() -> None:
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
    assert compute.pressure_summary is not None
    assert compute.pressure_summary.status is PressureSummaryStatus.OK
    assert compute.pressure_summary.is_ok
    assert not compute.pressure_summary.has_insufficient_pressure
    assert compute.pressure_summary.terminal_count == 2
    assert compute.pressure_summary.critical_node_id in {
        "N_EFS_A",
        "N_EFS_B",
    }
    assert compute.pressure_summary.worst_pressure_bar is not None
    assert compute.pressure_summary.pressure_margin_bar is not None
    assert compute.pressure_summary.pressure_margin_bar >= 0.0


def test_cold_water_pressure_diagnostic_detects_insufficient_pressure() -> None:
    network = domestic_water_branching_network()

    result = ColdWaterNetworkEngine.from_network(
        network=network,
        appliance_catalog=domestic_water_appliance_catalog(),
        pipe_catalog=domestic_water_pipe_catalog(),
        fluid_catalog=domestic_water_fluid_catalog(),
        singular_loss_catalog=domestic_water_singular_loss_catalog(),
    ).compute_all(
        source_node_id="N0",
        source_pressure_bar=0.8,
        min_required_pressure_bar=1.0,
    )

    assert result.ok
    assert result.value is not None

    compute = result.value

    assert compute.side is DomesticWaterSide.COLD_WATER
    assert compute.has_pressure_propagation
    assert compute.has_pressure_summary
    assert compute.pressure_summary is not None
    assert compute.pressure_summary.status is PressureSummaryStatus.INSUFFICIENT_PRESSURE
    assert not compute.pressure_summary.is_ok
    assert compute.pressure_summary.has_insufficient_pressure
    assert compute.pressure_summary.terminal_count == 2
    assert compute.pressure_summary.critical_node_id in {
        "N_EFS_A",
        "N_EFS_B",
    }
    assert compute.pressure_summary.worst_pressure_bar is not None
    assert compute.pressure_summary.worst_pressure_bar < 1.0
    assert compute.pressure_summary.pressure_margin_bar is not None
    assert compute.pressure_summary.pressure_margin_bar < 0.0

    worst_terminal = compute.pressure_summary.worst_terminal
    assert worst_terminal is not None
    assert worst_terminal.is_below_min
    assert worst_terminal.min_required_pressure_bar == 1.0
    assert worst_terminal.delta_to_min_bar == compute.pressure_summary.pressure_margin_bar


def test_hot_water_pressure_diagnostic_detects_insufficient_pressure() -> None:
    network = domestic_water_branching_network()

    result = HotWaterNetworkEngine.from_network(
        network=network,
        appliance_catalog=domestic_water_appliance_catalog(),
        pipe_catalog=domestic_water_pipe_catalog(),
        fluid_catalog=domestic_water_fluid_catalog(),
        singular_loss_catalog=domestic_water_singular_loss_catalog(),
    ).compute_all(
        source_node_id="N0",
        source_pressure_bar=0.8,
        min_required_pressure_bar=1.0,
    )

    assert result.ok
    assert result.value is not None

    compute = result.value

    assert compute.side is DomesticWaterSide.HOT_WATER
    assert compute.has_pressure_propagation
    assert compute.has_pressure_summary
    assert compute.pressure_summary is not None
    assert compute.pressure_summary.status is PressureSummaryStatus.INSUFFICIENT_PRESSURE
    assert not compute.pressure_summary.is_ok
    assert compute.pressure_summary.has_insufficient_pressure
    assert compute.pressure_summary.terminal_count == 2
    assert compute.pressure_summary.critical_node_id in {
        "N_ECS_A",
        "N_ECS_B",
    }
    assert compute.pressure_summary.worst_pressure_bar is not None
    assert compute.pressure_summary.worst_pressure_bar < 1.0
    assert compute.pressure_summary.pressure_margin_bar is not None
    assert compute.pressure_summary.pressure_margin_bar < 0.0

    worst_terminal = compute.pressure_summary.worst_terminal
    assert worst_terminal is not None
    assert worst_terminal.is_below_min
    assert worst_terminal.min_required_pressure_bar == 1.0
    assert worst_terminal.delta_to_min_bar == compute.pressure_summary.pressure_margin_bar


def test_pressure_diagnostic_keeps_cold_and_hot_networks_isolated() -> None:
    network = domestic_water_branching_network()

    cold_result = ColdWaterNetworkEngine.from_network(
        network=network,
        appliance_catalog=domestic_water_appliance_catalog(),
        pipe_catalog=domestic_water_pipe_catalog(),
        fluid_catalog=domestic_water_fluid_catalog(),
        singular_loss_catalog=domestic_water_singular_loss_catalog(),
    ).compute_all(
        source_node_id="N0",
        source_pressure_bar=0.8,
        min_required_pressure_bar=1.0,
    )

    hot_result = HotWaterNetworkEngine.from_network(
        network=network,
        appliance_catalog=domestic_water_appliance_catalog(),
        pipe_catalog=domestic_water_pipe_catalog(),
        fluid_catalog=domestic_water_fluid_catalog(),
        singular_loss_catalog=domestic_water_singular_loss_catalog(),
    ).compute_all(
        source_node_id="N0",
        source_pressure_bar=0.8,
        min_required_pressure_bar=1.0,
    )

    assert cold_result.ok
    assert hot_result.ok
    assert cold_result.value is not None
    assert hot_result.value is not None

    cold_summary = cold_result.value.pressure_summary
    hot_summary = hot_result.value.pressure_summary

    assert cold_summary is not None
    assert hot_summary is not None

    assert cold_summary.status is PressureSummaryStatus.INSUFFICIENT_PRESSURE
    assert hot_summary.status is PressureSummaryStatus.INSUFFICIENT_PRESSURE

    assert cold_summary.critical_node_id in {
        "N_EFS_A",
        "N_EFS_B",
    }
    assert hot_summary.critical_node_id in {
        "N_ECS_A",
        "N_ECS_B",
    }

    assert set(cold_result.value.section_results) == {
        "S_EFS_MAIN",
        "S_EFS_A",
        "S_EFS_B",
    }
    assert set(hot_result.value.section_results) == {
        "S_ECS_MAIN",
        "S_ECS_A",
        "S_ECS_B",
    }