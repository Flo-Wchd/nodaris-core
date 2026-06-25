from __future__ import annotations

from ndc_core.common.messages import EngineMessage
from ndc_core.networks.domestic_water.network_compute_result import (
    DomesticWaterNetworkComputeResult,
    DomesticWaterSectionComputeResult,
)
from ndc_core.networks.domestic_water.network_diagnostic import (
    DomesticWaterNetworkDiagnosticStatus,
    build_domestic_water_network_diagnostic,
)
from ndc_core.networks.domestic_water.pressure_network_result import (
    DomesticWaterPressurePropagationResult,
    DomesticWaterPressureSummary,
    NodePressureState,
    PressureSummaryStatus,
    TerminalPressureStatus,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


def test_network_diagnostic_not_computed() -> None:
    diagnostic = build_domestic_water_network_diagnostic(None)

    assert diagnostic.status is DomesticWaterNetworkDiagnosticStatus.NOT_COMPUTED
    assert not diagnostic.is_computed
    assert not diagnostic.is_ok
    assert diagnostic.side is None
    assert diagnostic.section_count == 0
    assert diagnostic.warning_count == 0
    assert diagnostic.error_count == 0
    assert diagnostic.pressure_status is None
    assert diagnostic.critical_node_id is None
    assert diagnostic.worst_pressure_bar is None
    assert diagnostic.pressure_margin_bar is None


def test_network_diagnostic_ok_without_pressure_summary() -> None:
    compute = DomesticWaterNetworkComputeResult(
        side=DomesticWaterSide.COLD_WATER,
        section_results={
            "S1": DomesticWaterSectionComputeResult(section_id="S1"),
        },
    )

    diagnostic = build_domestic_water_network_diagnostic(compute)

    assert diagnostic.status is DomesticWaterNetworkDiagnosticStatus.OK
    assert diagnostic.is_ok
    assert diagnostic.is_computed
    assert diagnostic.side is DomesticWaterSide.COLD_WATER
    assert diagnostic.section_count == 1
    assert diagnostic.sized_section_count == 0
    assert diagnostic.pressure_loss_section_count == 0
    assert diagnostic.warning_count == 0
    assert diagnostic.error_count == 0
    assert diagnostic.pressure_status is None


def test_network_diagnostic_warning_status() -> None:
    warning = EngineMessage.warning(
        code="DOMESTIC_WATER_TEST_WARNING",
        text="Warning for diagnostic test.",
    )
    compute = DomesticWaterNetworkComputeResult(
        side=DomesticWaterSide.COLD_WATER,
        section_results={},
        messages=(warning,),
    )

    diagnostic = build_domestic_water_network_diagnostic(compute)

    assert diagnostic.status is DomesticWaterNetworkDiagnosticStatus.WARNINGS
    assert not diagnostic.is_ok
    assert diagnostic.has_warnings
    assert not diagnostic.has_errors
    assert diagnostic.warning_count == 1
    assert diagnostic.error_count == 0
    assert diagnostic.messages == (warning,)


def test_network_diagnostic_error_status_has_priority() -> None:
    error = EngineMessage.error(
        code="DOMESTIC_WATER_TEST_ERROR",
        text="Error for diagnostic test.",
    )
    pressure_summary = _pressure_summary(
        status=PressureSummaryStatus.INSUFFICIENT_PRESSURE,
        critical_node_id="N1",
        worst_pressure_bar=0.8,
        pressure_margin_bar=-0.2,
    )
    compute = DomesticWaterNetworkComputeResult(
        side=DomesticWaterSide.COLD_WATER,
        section_results={},
        pressure_summary=pressure_summary,
        messages=(error,),
    )

    diagnostic = build_domestic_water_network_diagnostic(compute)

    assert diagnostic.status is DomesticWaterNetworkDiagnosticStatus.ERRORS
    assert diagnostic.has_errors
    assert diagnostic.error_count == 1
    assert diagnostic.pressure_status is PressureSummaryStatus.INSUFFICIENT_PRESSURE
    assert diagnostic.critical_node_id == "N1"
    assert diagnostic.worst_pressure_bar == 0.8
    assert diagnostic.pressure_margin_bar == -0.2


def test_network_diagnostic_insufficient_pressure_status() -> None:
    pressure_summary = _pressure_summary(
        status=PressureSummaryStatus.INSUFFICIENT_PRESSURE,
        critical_node_id="N1",
        worst_pressure_bar=0.8,
        pressure_margin_bar=-0.2,
    )
    compute = DomesticWaterNetworkComputeResult(
        side=DomesticWaterSide.HOT_WATER,
        section_results={},
        pressure_summary=pressure_summary,
    )

    diagnostic = build_domestic_water_network_diagnostic(compute)

    assert (
        diagnostic.status
        is DomesticWaterNetworkDiagnosticStatus.INSUFFICIENT_PRESSURE
    )
    assert diagnostic.has_insufficient_pressure
    assert not diagnostic.is_ok
    assert not diagnostic.has_warnings
    assert not diagnostic.has_errors
    assert diagnostic.side is DomesticWaterSide.HOT_WATER
    assert diagnostic.pressure_status is PressureSummaryStatus.INSUFFICIENT_PRESSURE
    assert diagnostic.critical_node_id == "N1"
    assert diagnostic.worst_pressure_bar == 0.8
    assert diagnostic.pressure_margin_bar == -0.2


def test_network_diagnostic_status_values() -> None:
    assert DomesticWaterNetworkDiagnosticStatus.OK.value == "ok"
    assert DomesticWaterNetworkDiagnosticStatus.WARNINGS.value == "warnings"
    assert DomesticWaterNetworkDiagnosticStatus.ERRORS.value == "errors"
    assert (
        DomesticWaterNetworkDiagnosticStatus.INSUFFICIENT_PRESSURE.value
        == "insufficient_pressure"
    )
    assert DomesticWaterNetworkDiagnosticStatus.NOT_COMPUTED.value == "not_computed"


def _pressure_summary(
    *,
    status: PressureSummaryStatus,
    critical_node_id: str,
    worst_pressure_bar: float,
    pressure_margin_bar: float,
) -> DomesticWaterPressureSummary:
    propagation = DomesticWaterPressurePropagationResult(
        source_node_id="N0",
        source_pressure_pa=300_000.0,
        source_pressure_bar=3.0,
        side=DomesticWaterSide.COLD_WATER,
        node_pressures={
            critical_node_id: NodePressureState(
                node_id=critical_node_id,
                pressure_pa=worst_pressure_bar * 100_000.0,
                pressure_bar=worst_pressure_bar,
                is_terminal=True,
            ),
        },
    )
    terminal = TerminalPressureStatus(
        node_id=critical_node_id,
        pressure_pa=worst_pressure_bar * 100_000.0,
        pressure_bar=worst_pressure_bar,
        min_required_pressure_bar=worst_pressure_bar - pressure_margin_bar,
        delta_to_min_bar=pressure_margin_bar,
        is_below_min=pressure_margin_bar < 0.0,
    )

    return DomesticWaterPressureSummary(
        source_node_id="N0",
        source_pressure_bar=3.0,
        min_required_pressure_bar=terminal.min_required_pressure_bar,
        side=DomesticWaterSide.COLD_WATER,
        worst_terminal=terminal,
        terminal_statuses={critical_node_id: terminal},
        propagation=propagation,
        status=status,
    )