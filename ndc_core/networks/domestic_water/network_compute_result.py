from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from ndc_core.common.messages import EngineMessage
from ndc_core.networks.domestic_water.pressure_loss_result import (
    DomesticWaterPressureLossResult,
)
from ndc_core.networks.domestic_water.pressure_network import (
    DomesticWaterPressurePropagationResult,
    DomesticWaterPressureSummary,
)
from ndc_core.networks.domestic_water.section_sizing import (
    DomesticWaterSectionSizing,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


class DomesticWaterNetworkStep(StrEnum):
    """Network compute step names."""

    TOPOLOGY_VALIDATION = "topology_validation"
    SIZING = "sizing"
    PRESSURE_LOSS = "pressure_loss"
    PRESSURE_PROPAGATION = "pressure_propagation"
    PRESSURE_SUMMARY = "pressure_summary"


@dataclass(frozen=True, slots=True)
class DomesticWaterSectionComputeResult:
    """Consolidated compute result for one section."""

    section_id: str
    sizing: DomesticWaterSectionSizing | None = None
    pressure_loss: DomesticWaterPressureLossResult | None = None
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @property
    def sizing_ok(self) -> bool:
        return self.sizing is not None and not self.sizing.has_errors

    @property
    def pressure_loss_ok(self) -> bool:
        return self.pressure_loss is not None and not self.pressure_loss.has_errors

    @property
    def has_pressure_loss(self) -> bool:
        return self.pressure_loss is not None

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)


@dataclass(frozen=True, slots=True)
class DomesticWaterNetworkComputeResult:
    """Consolidated network compute result."""

    side: DomesticWaterSide
    section_results: dict[str, DomesticWaterSectionComputeResult]
    appliance_propagation: object | None = None
    pressure_propagation: DomesticWaterPressurePropagationResult | None = None
    pressure_summary: DomesticWaterPressureSummary | None = None
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @property
    def section_count(self) -> int:
        return len(self.section_results)

    @property
    def sized_section_count(self) -> int:
        return sum(1 for result in self.section_results.values() if result.sizing_ok)

    @property
    def pressure_loss_section_count(self) -> int:
        return sum(
            1
            for result in self.section_results.values()
            if result.pressure_loss_ok
        )

    @property
    def has_pressure_propagation(self) -> bool:
        return self.pressure_propagation is not None

    @property
    def has_pressure_summary(self) -> bool:
        return self.pressure_summary is not None

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)