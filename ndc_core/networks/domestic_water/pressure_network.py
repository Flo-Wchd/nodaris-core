from __future__ import annotations

from collections import deque
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.hydraulics.conversions import pressure_bar_to_pa, pressure_pa_to_bar
from ndc_core.networks.domestic_water.types import DomesticWaterSide
from ndc_core.networks.domestic_water.side_matching import (
    node_is_terminal_for_domestic_water_side,
    section_matches_domestic_water_side,
)
from ndc_core.networks.domestic_water.entity_access import (
    apply_node_pressures,
    apply_section_pressures,
    clean_optional_code,
    read_downstream_section_ids,
    read_section_pressure_loss_pa,
)
from ndc_core.networks.domestic_water.numeric import (
    safe_non_negative_float,
    safe_pressure_pa,
)
from ndc_core.networks.domestic_water.pressure_network_result import (
    DomesticWaterPressurePropagationResult,
    DomesticWaterPressureSummary,
    NodePressureState,
    PressurePropagationStatus,
    TerminalPressureStatus,
)


@dataclass(frozen=True, slots=True)
class DomesticWaterPressureNetworkEngine:
    """
    Common EFS/ECS pressure propagation engine.

    This engine does not compute section pressure losses. It only consumes:

        Section.total_pressure_loss_pa

    Convention:

        p_down = p_up - total_pressure_loss_pa

    If total_pressure_loss_pa is negative, downstream pressure increases.
    """

    nodes: Mapping[str, Any]
    sections: Mapping[str, Any]
    side: DomesticWaterSide = DomesticWaterSide.COLD_WATER

    def propagate_pressures(
        self,
        *,
        source_node_id: str,
        source_pressure_pa: float,
    ) -> Result[DomesticWaterPressurePropagationResult]:
        messages: list[EngineMessage] = []

        source_id = str(source_node_id or "").strip()
        if not source_id:
            messages.append(
                EngineMessage.error(
                    code="DOMESTIC_WATER_PRESSURE_SOURCE_EMPTY",
                    text="Source node id is empty; pressure propagation cannot start.",
                    context={},
                )
            )
            return Result.failure(messages=messages)

        if source_id not in self.nodes:
            messages.append(
                EngineMessage.error(
                    code="DOMESTIC_WATER_PRESSURE_SOURCE_NOT_FOUND",
                    text="Source node was not found; pressure propagation cannot start.",
                    context={"source_node_id": source_id},
                )
            )
            result = DomesticWaterPressurePropagationResult(
                source_node_id=source_id,
                source_pressure_pa=0.0,
                source_pressure_bar=0.0,
                side=self.side,
                node_pressures={},
                messages=tuple(messages),
                status=PressurePropagationStatus.SOURCE_NOT_FOUND,
            )
            return Result.failure(value=result, messages=messages)

        source_pressure = safe_pressure_pa(source_pressure_pa)

        pressures_pa: dict[str, float] = {source_id: source_pressure}
        queue: deque[str] = deque([source_id])
        warned_missing_losses: set[str] = set()

        while queue:
            current_node_id = queue.popleft()
            current_pressure_pa = pressures_pa.get(current_node_id, 0.0)

            node = self.nodes.get(current_node_id)
            downstream_section_ids = read_downstream_section_ids(node)

            for section_id in downstream_section_ids:
                section = self.sections.get(section_id)
                if section is None:
                    messages.append(
                        EngineMessage.warning(
                            code="DOMESTIC_WATER_PRESSURE_SECTION_NOT_FOUND",
                            text="Section referenced by node was not found.",
                            context={
                                "node_id": current_node_id,
                                "section_id": section_id,
                            },
                        )
                    )
                    continue

                if not section_matches_domestic_water_side(section, self.side):
                    continue

                downstream_node_id = clean_optional_code(
                    getattr(section, "downstream_node_id", None)
                )
                if downstream_node_id is None:
                    messages.append(
                        EngineMessage.warning(
                            code="DOMESTIC_WATER_PRESSURE_DOWNSTREAM_NODE_MISSING",
                            text="Section has no downstream node; pressure propagation skipped.",
                            context={"section_id": section_id},
                        )
                    )
                    continue

                pressure_loss_read = read_section_pressure_loss_pa(section)

                if pressure_loss_read.missing:
                    if section_id not in warned_missing_losses:
                        messages.append(
                            EngineMessage.warning(
                                code="DOMESTIC_WATER_PRESSURE_LOSS_MISSING",
                                text="Section pressure loss is missing; propagation uses Δp = 0.",
                                context={"section_id": section_id},
                            )
                        )
                        warned_missing_losses.add(section_id)

                elif pressure_loss_read.invalid:
                    messages.append(
                        EngineMessage.warning(
                            code="DOMESTIC_WATER_PRESSURE_LOSS_INVALID",
                            text="Section pressure loss is invalid; propagation uses Δp = 0.",
                            context={
                                "section_id": section_id,
                                "value": pressure_loss_read.raw_value,
                            },
                        )
                    )

                elif pressure_loss_read.not_finite:
                    messages.append(
                        EngineMessage.warning(
                            code="DOMESTIC_WATER_PRESSURE_LOSS_NOT_FINITE",
                            text="Section pressure loss is not finite; propagation uses Δp = 0.",
                            context={
                                "section_id": section_id,
                                "value": pressure_loss_read.raw_value,
                            },
                        )
                    )

                delta_p_pa = pressure_loss_read.pressure_loss_pa

                downstream_pressure_pa = max(0.0, current_pressure_pa - delta_p_pa)

                apply_section_pressures(
                    section=section,
                    pressure_start_pa=current_pressure_pa,
                    pressure_end_pa=downstream_pressure_pa,
                )

                previous_pressure = pressures_pa.get(downstream_node_id)

                if (
                    previous_pressure is None
                    or downstream_pressure_pa < previous_pressure
                ):
                    pressures_pa[downstream_node_id] = downstream_pressure_pa
                    queue.append(downstream_node_id)

        node_states = {
            node_id: NodePressureState(
                node_id=node_id,
                pressure_pa=pressure_pa,
                pressure_bar=pressure_pa_to_bar(pressure_pa),
                is_terminal=node_is_terminal_for_domestic_water_side(
                    node=self.nodes.get(node_id),
                    sections=self.sections,
                    side=self.side,
                ),
            )
            for node_id, pressure_pa in pressures_pa.items()
        }

        apply_node_pressures(self.nodes, node_states)

        result = DomesticWaterPressurePropagationResult(
            source_node_id=source_id,
            source_pressure_pa=source_pressure,
            source_pressure_bar=pressure_pa_to_bar(source_pressure),
            side=self.side,
            node_pressures=node_states,
            messages=tuple(messages),
            status=PressurePropagationStatus.SUCCESS,
        )

        return Result.success(value=result, messages=messages)

    def summarize_worst_terminal_pressure(
        self,
        *,
        source_node_id: str,
        source_pressure_bar: float,
        min_required_pressure_bar: float = 1.0,
    ) -> Result[DomesticWaterPressureSummary]:
        messages: list[EngineMessage] = []

        source_pressure_bar_f = safe_non_negative_float(source_pressure_bar)
        min_required_bar_f = safe_non_negative_float(
            min_required_pressure_bar,
            default=1.0,
        )

        propagation_result = self.propagate_pressures(
            source_node_id=source_node_id,
            source_pressure_pa=pressure_bar_to_pa(source_pressure_bar_f),
        )

        messages.extend(propagation_result.messages)

        if propagation_result.value is None:
            summary = DomesticWaterPressureSummary(
                source_node_id=str(source_node_id or "").strip(),
                source_pressure_bar=source_pressure_bar_f,
                min_required_pressure_bar=min_required_bar_f,
                side=self.side,
                worst_terminal=None,
                terminal_statuses={},
                propagation=DomesticWaterPressurePropagationResult(
                    source_node_id=str(source_node_id or "").strip(),
                    source_pressure_pa=0.0,
                    source_pressure_bar=0.0,
                    side=self.side,
                    node_pressures={},
                    messages=tuple(messages),
                    status=PressurePropagationStatus.SOURCE_NOT_FOUND,
                ),
                messages=tuple(messages),
            )
            return Result.failure(value=summary, messages=messages)

        terminal_statuses: dict[str, TerminalPressureStatus] = {}

        for node_id, state in propagation_result.value.node_pressures.items():
            if not state.is_terminal:
                continue

            delta_to_min = state.pressure_bar - min_required_bar_f

            terminal_statuses[node_id] = TerminalPressureStatus(
                node_id=node_id,
                pressure_pa=state.pressure_pa,
                pressure_bar=state.pressure_bar,
                min_required_pressure_bar=min_required_bar_f,
                delta_to_min_bar=delta_to_min,
                is_below_min=delta_to_min < 0.0,
            )

        if not terminal_statuses:
            messages.append(
                EngineMessage.warning(
                    code="DOMESTIC_WATER_PRESSURE_NO_TERMINAL_REACHED",
                    text="No terminal node was reached during pressure propagation.",
                    context={"source_node_id": str(source_node_id or "").strip()},
                )
            )
            summary = DomesticWaterPressureSummary(
                source_node_id=propagation_result.value.source_node_id,
                source_pressure_bar=source_pressure_bar_f,
                min_required_pressure_bar=min_required_bar_f,
                side=self.side,
                worst_terminal=None,
                terminal_statuses={},
                propagation=propagation_result.value,
                messages=tuple(messages),
            )
            return Result.partial(value=summary, messages=messages)

        worst_terminal = min(
            terminal_statuses.values(),
            key=lambda terminal: terminal.delta_to_min_bar,
        )

        summary = DomesticWaterPressureSummary(
            source_node_id=propagation_result.value.source_node_id,
            source_pressure_bar=source_pressure_bar_f,
            min_required_pressure_bar=min_required_bar_f,
            side=self.side,
            worst_terminal=worst_terminal,
            terminal_statuses=terminal_statuses,
            propagation=propagation_result.value,
            messages=tuple(messages),
        )

        return Result.success(value=summary, messages=messages)


def propagate_cold_water_pressures(
    *,
    nodes: Mapping[str, Any],
    sections: Mapping[str, Any],
    source_node_id: str,
    source_pressure_pa: float,
) -> Result[DomesticWaterPressurePropagationResult]:
    """Convenience function for EFS pressure propagation."""

    return DomesticWaterPressureNetworkEngine(
        nodes=nodes,
        sections=sections,
        side=DomesticWaterSide.COLD_WATER,
    ).propagate_pressures(
        source_node_id=source_node_id,
        source_pressure_pa=source_pressure_pa,
    )


def propagate_hot_water_pressures(
    *,
    nodes: Mapping[str, Any],
    sections: Mapping[str, Any],
    source_node_id: str,
    source_pressure_pa: float,
) -> Result[DomesticWaterPressurePropagationResult]:
    """Convenience function for ECS forward pressure propagation."""

    return DomesticWaterPressureNetworkEngine(
        nodes=nodes,
        sections=sections,
        side=DomesticWaterSide.HOT_WATER,
    ).propagate_pressures(
        source_node_id=source_node_id,
        source_pressure_pa=source_pressure_pa,
    )


def summarize_cold_water_worst_terminal_pressure(
    *,
    nodes: Mapping[str, Any],
    sections: Mapping[str, Any],
    source_node_id: str,
    source_pressure_bar: float,
    min_required_pressure_bar: float = 1.0,
) -> Result[DomesticWaterPressureSummary]:
    """Convenience function for EFS worst terminal summary."""

    return DomesticWaterPressureNetworkEngine(
        nodes=nodes,
        sections=sections,
        side=DomesticWaterSide.COLD_WATER,
    ).summarize_worst_terminal_pressure(
        source_node_id=source_node_id,
        source_pressure_bar=source_pressure_bar,
        min_required_pressure_bar=min_required_pressure_bar,
    )


def summarize_hot_water_worst_terminal_pressure(
    *,
    nodes: Mapping[str, Any],
    sections: Mapping[str, Any],
    source_node_id: str,
    source_pressure_bar: float,
    min_required_pressure_bar: float = 1.0,
) -> Result[DomesticWaterPressureSummary]:
    """Convenience function for ECS forward worst terminal summary."""

    return DomesticWaterPressureNetworkEngine(
        nodes=nodes,
        sections=sections,
        side=DomesticWaterSide.HOT_WATER,
    ).summarize_worst_terminal_pressure(
        source_node_id=source_node_id,
        source_pressure_bar=source_pressure_bar,
        min_required_pressure_bar=min_required_pressure_bar,
    )