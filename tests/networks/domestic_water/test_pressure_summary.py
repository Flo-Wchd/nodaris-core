from __future__ import annotations

from ndc_core.common.messages import EngineMessage
from ndc_core.networks.domestic_water.pressure_network_result import (
    DomesticWaterPressurePropagationResult,
    NodePressureState,
    PressurePropagationStatus,
    PressureSummaryStatus,
)
from ndc_core.networks.domestic_water.pressure_summary import (
    build_pressure_summary_from_propagation,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


def _propagation(
    *,
    node_pressures: dict[str, NodePressureState],
    status: PressurePropagationStatus = PressurePropagationStatus.SUCCESS,
) -> DomesticWaterPressurePropagationResult:
    return DomesticWaterPressurePropagationResult(
        source_node_id="A",
        source_pressure_pa=300_000.0,
        source_pressure_bar=3.0,
        side=DomesticWaterSide.COLD_WATER,
        node_pressures=node_pressures,
        status=status,
    )


def test_build_pressure_summary_ok_status() -> None:
    result = build_pressure_summary_from_propagation(
        propagation=_propagation(
            node_pressures={
                "A": NodePressureState(
                    node_id="A",
                    pressure_pa=300_000.0,
                    pressure_bar=3.0,
                ),
                "B": NodePressureState(
                    node_id="B",
                    pressure_pa=275_000.0,
                    pressure_bar=2.75,
                    is_terminal=True,
                ),
            }
        ),
        source_pressure_bar=3.0,
        min_required_pressure_bar=2.5,
        side=DomesticWaterSide.COLD_WATER,
        messages=[],
    )

    assert result.ok
    assert result.value is not None
    assert result.value.status is PressureSummaryStatus.OK
    assert result.value.is_ok
    assert not result.value.has_insufficient_pressure
    assert result.value.terminal_count == 1
    assert result.value.critical_node_id == "B"
    assert result.value.worst_pressure_bar == 2.75
    assert result.value.pressure_margin_bar == 0.25


def test_build_pressure_summary_insufficient_pressure_status() -> None:
    result = build_pressure_summary_from_propagation(
        propagation=_propagation(
            node_pressures={
                "B": NodePressureState(
                    node_id="B",
                    pressure_pa=240_000.0,
                    pressure_bar=2.4,
                    is_terminal=True,
                ),
            }
        ),
        source_pressure_bar=3.0,
        min_required_pressure_bar=2.5,
        side=DomesticWaterSide.COLD_WATER,
        messages=[],
    )

    assert result.ok
    assert result.value is not None
    assert result.value.status is PressureSummaryStatus.INSUFFICIENT_PRESSURE
    assert not result.value.is_ok
    assert result.value.has_insufficient_pressure
    assert result.value.critical_node_id == "B"
    assert round(result.value.pressure_margin_bar or 0.0, 2) == -0.1


def test_build_pressure_summary_keeps_most_unfavorable_terminal() -> None:
    result = build_pressure_summary_from_propagation(
        propagation=_propagation(
            node_pressures={
                "B": NodePressureState(
                    node_id="B",
                    pressure_pa=260_000.0,
                    pressure_bar=2.6,
                    is_terminal=True,
                ),
                "C": NodePressureState(
                    node_id="C",
                    pressure_pa=245_000.0,
                    pressure_bar=2.45,
                    is_terminal=True,
                ),
            }
        ),
        source_pressure_bar=3.0,
        min_required_pressure_bar=2.5,
        side=DomesticWaterSide.COLD_WATER,
        messages=[],
    )

    assert result.ok
    assert result.value is not None
    assert result.value.status is PressureSummaryStatus.INSUFFICIENT_PRESSURE
    assert result.value.terminal_count == 2
    assert result.value.critical_node_id == "C"
    assert result.value.worst_pressure_bar == 2.45
    assert round(result.value.pressure_margin_bar or 0.0, 2) == -0.05


def test_build_pressure_summary_no_terminal_reached_status() -> None:
    result = build_pressure_summary_from_propagation(
        propagation=_propagation(
            node_pressures={
                "A": NodePressureState(
                    node_id="A",
                    pressure_pa=300_000.0,
                    pressure_bar=3.0,
                    is_terminal=False,
                ),
            }
        ),
        source_pressure_bar=3.0,
        min_required_pressure_bar=1.0,
        side=DomesticWaterSide.COLD_WATER,
        messages=[],
    )

    assert result.ok
    assert result.has_warnings
    assert result.value is not None
    assert result.value.status is PressureSummaryStatus.NO_TERMINAL_REACHED
    assert not result.value.has_worst_terminal
    assert result.value.terminal_count == 0
    assert result.value.critical_node_id is None
    assert result.value.worst_pressure_bar is None
    assert result.value.pressure_margin_bar is None
    assert any(
        message.code == "DOMESTIC_WATER_PRESSURE_NO_TERMINAL_REACHED"
        for message in result.messages
    )


def test_build_pressure_summary_source_not_found_status() -> None:
    error = EngineMessage.error(
        code="DOMESTIC_WATER_PRESSURE_SOURCE_NOT_FOUND",
        text="Source node was not found.",
        context={"source_node_id": "UNKNOWN"},
    )

    result = build_pressure_summary_from_propagation(
        propagation=DomesticWaterPressurePropagationResult(
            source_node_id="UNKNOWN",
            source_pressure_pa=0.0,
            source_pressure_bar=0.0,
            side=DomesticWaterSide.COLD_WATER,
            node_pressures={},
            messages=(error,),
            status=PressurePropagationStatus.SOURCE_NOT_FOUND,
        ),
        source_pressure_bar=3.0,
        min_required_pressure_bar=1.0,
        side=DomesticWaterSide.COLD_WATER,
        messages=[error],
    )

    assert result.failed
    assert result.value is not None
    assert result.value.status is PressureSummaryStatus.SOURCE_NOT_FOUND
    assert not result.value.has_worst_terminal
    assert result.value.terminal_count == 0
    assert result.value.propagation.status is PressurePropagationStatus.SOURCE_NOT_FOUND