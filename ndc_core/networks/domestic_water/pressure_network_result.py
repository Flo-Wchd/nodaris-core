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

    @property
    def has_worst_terminal(self) -> bool:
        return self.worst_terminal is not None

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)