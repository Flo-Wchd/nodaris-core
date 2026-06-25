from __future__ import annotations

from collections.abc import Sequence

from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.networks.domestic_water.pressure_network_result import (
    DomesticWaterPressurePropagationResult,
    DomesticWaterPressureSummary,
    PressurePropagationStatus,
    PressureSummaryStatus,
    TerminalPressureStatus,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


def build_pressure_summary_from_propagation(
    *,
    propagation: DomesticWaterPressurePropagationResult,
    source_pressure_bar: float,
    min_required_pressure_bar: float,
    side: DomesticWaterSide,
    messages: Sequence[EngineMessage],
) -> Result[DomesticWaterPressureSummary]:
    """
    Build a managed worst-terminal pressure summary from propagation results.

    This is the single place responsible for:
    - terminal pressure checks;
    - critical terminal selection;
    - pressure margin calculation;
    - business status selection.
    """

    summary_messages = list(messages)

    if propagation.status is PressurePropagationStatus.SOURCE_NOT_FOUND:
        summary = DomesticWaterPressureSummary(
            source_node_id=propagation.source_node_id,
            source_pressure_bar=source_pressure_bar,
            min_required_pressure_bar=min_required_pressure_bar,
            side=side,
            worst_terminal=None,
            terminal_statuses={},
            propagation=propagation,
            messages=tuple(summary_messages),
            status=PressureSummaryStatus.SOURCE_NOT_FOUND,
        )
        return Result.failure(value=summary, messages=summary_messages)

    terminal_statuses = _build_terminal_statuses(
        propagation=propagation,
        min_required_pressure_bar=min_required_pressure_bar,
    )

    if not terminal_statuses:
        summary_messages.append(
            EngineMessage.warning(
                code="DOMESTIC_WATER_PRESSURE_NO_TERMINAL_REACHED",
                text="No terminal node was reached during pressure propagation.",
                context={"source_node_id": propagation.source_node_id},
            )
        )
        summary = DomesticWaterPressureSummary(
            source_node_id=propagation.source_node_id,
            source_pressure_bar=source_pressure_bar,
            min_required_pressure_bar=min_required_pressure_bar,
            side=side,
            worst_terminal=None,
            terminal_statuses={},
            propagation=propagation,
            messages=tuple(summary_messages),
            status=PressureSummaryStatus.NO_TERMINAL_REACHED,
        )
        return Result.partial(value=summary, messages=summary_messages)

    worst_terminal = min(
        terminal_statuses.values(),
        key=lambda terminal: terminal.delta_to_min_bar,
    )
    summary_status = (
        PressureSummaryStatus.INSUFFICIENT_PRESSURE
        if worst_terminal.is_below_min
        else PressureSummaryStatus.OK
    )

    summary = DomesticWaterPressureSummary(
        source_node_id=propagation.source_node_id,
        source_pressure_bar=source_pressure_bar,
        min_required_pressure_bar=min_required_pressure_bar,
        side=side,
        worst_terminal=worst_terminal,
        terminal_statuses=terminal_statuses,
        propagation=propagation,
        messages=tuple(summary_messages),
        status=summary_status,
    )

    return Result.success(value=summary, messages=summary_messages)


def _build_terminal_statuses(
    *,
    propagation: DomesticWaterPressurePropagationResult,
    min_required_pressure_bar: float,
) -> dict[str, TerminalPressureStatus]:
    terminal_statuses: dict[str, TerminalPressureStatus] = {}

    for node_id, state in propagation.node_pressures.items():
        if not state.is_terminal:
            continue

        delta_to_min = state.pressure_bar - min_required_pressure_bar

        terminal_statuses[node_id] = TerminalPressureStatus(
            node_id=node_id,
            pressure_pa=state.pressure_pa,
            pressure_bar=state.pressure_bar,
            min_required_pressure_bar=min_required_pressure_bar,
            delta_to_min_bar=delta_to_min,
            is_below_min=delta_to_min < 0.0,
        )

    return terminal_statuses