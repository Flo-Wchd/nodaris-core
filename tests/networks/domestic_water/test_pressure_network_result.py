from __future__ import annotations

from ndc_core.common.messages import EngineMessage
from ndc_core.networks.domestic_water.pressure_network import (
    DomesticWaterPressurePropagationResult as EnginePressurePropagationResult,
)
from ndc_core.networks.domestic_water.pressure_network import (
    DomesticWaterPressureSummary as EnginePressureSummary,
)
from ndc_core.networks.domestic_water.pressure_network import (
    NodePressureState as EngineNodePressureState,
)
from ndc_core.networks.domestic_water.pressure_network import (
    PressurePropagationStatus as EnginePressurePropagationStatus,
)
from ndc_core.networks.domestic_water.pressure_network import (
    TerminalPressureStatus as EngineTerminalPressureStatus,
)
from ndc_core.networks.domestic_water.pressure_network_result import (
    DomesticWaterPressurePropagationResult,
    DomesticWaterPressureSummary,
    NodePressureState,
    PressurePropagationStatus,
    TerminalPressureStatus,
    PressureSummaryStatus,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide
from ndc_core.networks.domestic_water.pressure_network import (
    PressureSummaryStatus as EnginePressureSummaryStatus,
)


def test_pressure_network_result_exports_are_kept_from_pressure_network() -> None:
    assert EnginePressurePropagationResult is DomesticWaterPressurePropagationResult
    assert EnginePressureSummary is DomesticWaterPressureSummary
    assert EngineNodePressureState is NodePressureState
    assert EnginePressurePropagationStatus is PressurePropagationStatus
    assert EngineTerminalPressureStatus is TerminalPressureStatus
    assert EnginePressureSummaryStatus is PressureSummaryStatus


def test_pressure_propagation_status_values() -> None:
    assert PressurePropagationStatus.SUCCESS.value == "success"
    assert PressurePropagationStatus.SOURCE_NOT_FOUND.value == "source_not_found"
    assert PressurePropagationStatus.NO_TERMINAL_REACHED.value == "no_terminal_reached"


def test_pressure_propagation_result_helpers() -> None:
    warning = EngineMessage.warning(
        code="TEST_WARNING",
        text="Test warning.",
        context={"node_id": "B"},
    )

    result = DomesticWaterPressurePropagationResult(
        source_node_id="A",
        source_pressure_pa=300_000.0,
        source_pressure_bar=3.0,
        side=DomesticWaterSide.COLD_WATER,
        node_pressures={
            "A": NodePressureState(
                node_id="A",
                pressure_pa=300_000.0,
                pressure_bar=3.0,
            ),
            "B": NodePressureState(
                node_id="B",
                pressure_pa=250_000.0,
                pressure_bar=2.5,
                is_terminal=True,
            ),
        },
        messages=(warning,),
    )

    assert result.reached_node_ids == ("A", "B")
    assert result.has_warnings
    assert not result.has_errors


def test_pressure_propagation_result_error_helper() -> None:
    error = EngineMessage.error(
        code="TEST_ERROR",
        text="Test error.",
        context={"source_node_id": "A"},
    )

    result = DomesticWaterPressurePropagationResult(
        source_node_id="A",
        source_pressure_pa=0.0,
        source_pressure_bar=0.0,
        side=DomesticWaterSide.COLD_WATER,
        node_pressures={},
        messages=(error,),
        status=PressurePropagationStatus.SOURCE_NOT_FOUND,
    )

    assert result.reached_node_ids == ()
    assert not result.has_warnings
    assert result.has_errors


def test_pressure_summary_helpers() -> None:
    propagation = DomesticWaterPressurePropagationResult(
        source_node_id="A",
        source_pressure_pa=300_000.0,
        source_pressure_bar=3.0,
        side=DomesticWaterSide.COLD_WATER,
        node_pressures={
            "B": NodePressureState(
                node_id="B",
                pressure_pa=250_000.0,
                pressure_bar=2.5,
                is_terminal=True,
            ),
        },
    )
    terminal = TerminalPressureStatus(
        node_id="B",
        pressure_pa=250_000.0,
        pressure_bar=2.5,
        min_required_pressure_bar=2.6,
        delta_to_min_bar=-0.1,
        is_below_min=True,
    )

    summary = DomesticWaterPressureSummary(
        source_node_id="A",
        source_pressure_bar=3.0,
        min_required_pressure_bar=2.6,
        side=DomesticWaterSide.COLD_WATER,
        worst_terminal=terminal,
        terminal_statuses={"B": terminal},
        propagation=propagation,
    )

    assert summary.has_worst_terminal
    assert not summary.has_warnings
    assert not summary.has_errors
    assert summary.status is PressureSummaryStatus.OK
    assert summary.is_ok
    assert not summary.has_insufficient_pressure
    assert summary.terminal_count == 1
    assert summary.has_terminal_pressure_checks
    assert summary.critical_node_id == "B"
    assert summary.worst_pressure_bar == 2.5
    assert summary.pressure_margin_bar == -0.1


def test_pressure_summary_insufficient_pressure_helpers() -> None:
    propagation = DomesticWaterPressurePropagationResult(
        source_node_id="A",
        source_pressure_pa=300_000.0,
        source_pressure_bar=3.0,
        side=DomesticWaterSide.COLD_WATER,
        node_pressures={
            "B": NodePressureState(
                node_id="B",
                pressure_pa=250_000.0,
                pressure_bar=2.5,
                is_terminal=True,
            ),
        },
    )
    terminal = TerminalPressureStatus(
        node_id="B",
        pressure_pa=250_000.0,
        pressure_bar=2.5,
        min_required_pressure_bar=2.6,
        delta_to_min_bar=-0.1,
        is_below_min=True,
    )

    summary = DomesticWaterPressureSummary(
        source_node_id="A",
        source_pressure_bar=3.0,
        min_required_pressure_bar=2.6,
        side=DomesticWaterSide.COLD_WATER,
        worst_terminal=terminal,
        terminal_statuses={"B": terminal},
        propagation=propagation,
        status=PressureSummaryStatus.INSUFFICIENT_PRESSURE,
    )

    assert not summary.is_ok
    assert summary.has_insufficient_pressure
    assert summary.terminal_count == 1
    assert summary.critical_node_id == "B"
    assert summary.worst_pressure_bar == 2.5
    assert summary.pressure_margin_bar == -0.1