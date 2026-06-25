from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from ndc_core.common.messages import EngineMessage
from ndc_core.networks.domestic_water.types import DomesticWaterSide


class PressurePropagationStatus(StrEnum):
    """Pressure propagation status."""

    SUCCESS = "success"
    SOURCE_NOT_FOUND = "source_not_found"
    NO_TERMINAL_REACHED = "no_terminal_reached"


class PressureSummaryStatus(StrEnum):
    """Worst terminal pressure summary status."""

    OK = "ok"
    INSUFFICIENT_PRESSURE = "insufficient_pressure"
    NO_TERMINAL_REACHED = "no_terminal_reached"
    SOURCE_NOT_FOUND = "source_not_found"


@dataclass(frozen=True, slots=True)
class NodePressureState:
    """Computed pressure state for one node."""

    node_id: str
    pressure_pa: float
    pressure_bar: float
    is_terminal: bool = False
    min_required_pressure_bar: float | None = None
    delta_to_min_bar: float | None = None
    is_below_min: bool | None = None


@dataclass(frozen=True, slots=True)
class DomesticWaterPressurePropagationResult:
    """Network pressure propagation result."""

    source_node_id: str
    source_pressure_pa: float
    source_pressure_bar: float
    side: DomesticWaterSide
    node_pressures: dict[str, NodePressureState]
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)
    status: PressurePropagationStatus = PressurePropagationStatus.SUCCESS

    @property
    def reached_node_ids(self) -> tuple[str, ...]:
        return tuple(self.node_pressures)

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)


@dataclass(frozen=True, slots=True)
class TerminalPressureStatus:
    """Pressure status for one terminal node."""

    node_id: str
    pressure_pa: float
    pressure_bar: float
    min_required_pressure_bar: float
    delta_to_min_bar: float
    is_below_min: bool


@dataclass(frozen=True, slots=True)
class DomesticWaterPressureSummary:
    """Worst terminal pressure summary."""

    source_node_id: str
    source_pressure_bar: float
    min_required_pressure_bar: float
    side: DomesticWaterSide
    worst_terminal: TerminalPressureStatus | None
    terminal_statuses: dict[str, TerminalPressureStatus]
    propagation: DomesticWaterPressurePropagationResult
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)
    status: PressureSummaryStatus = PressureSummaryStatus.OK

    @property
    def has_worst_terminal(self) -> bool:
        return self.worst_terminal is not None

    @property
    def terminal_count(self) -> int:
        return len(self.terminal_statuses)

    @property
    def has_terminal_pressure_checks(self) -> bool:
        return bool(self.terminal_statuses)

    @property
    def critical_node_id(self) -> str | None:
        return self.worst_terminal.node_id if self.worst_terminal else None

    @property
    def worst_pressure_bar(self) -> float | None:
        return self.worst_terminal.pressure_bar if self.worst_terminal else None

    @property
    def pressure_margin_bar(self) -> float | None:
        return self.worst_terminal.delta_to_min_bar if self.worst_terminal else None

    @property
    def has_insufficient_pressure(self) -> bool:
        return self.status is PressureSummaryStatus.INSUFFICIENT_PRESSURE

    @property
    def is_ok(self) -> bool:
        return self.status is PressureSummaryStatus.OK

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)