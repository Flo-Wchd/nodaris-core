from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from ndc_core.common.messages import EngineMessage
from ndc_core.networks.domestic_water.network_compute_result import (
    DomesticWaterNetworkComputeResult,
)
from ndc_core.networks.domestic_water.pressure_network_result import (
    PressureSummaryStatus,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


class DomesticWaterNetworkDiagnosticStatus(StrEnum):
    """Consolidated domestic water network diagnostic status."""

    OK = "ok"
    WARNINGS = "warnings"
    ERRORS = "errors"
    INSUFFICIENT_PRESSURE = "insufficient_pressure"
    NOT_COMPUTED = "not_computed"


@dataclass(frozen=True, slots=True)
class DomesticWaterNetworkDiagnostic:
    """Consolidated diagnostic for GUI, reporting and export layers."""

    status: DomesticWaterNetworkDiagnosticStatus
    side: DomesticWaterSide | None
    section_count: int = 0
    sized_section_count: int = 0
    pressure_loss_section_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    pressure_status: PressureSummaryStatus | None = None
    critical_node_id: str | None = None
    worst_pressure_bar: float | None = None
    pressure_margin_bar: float | None = None
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @property
    def is_ok(self) -> bool:
        return self.status is DomesticWaterNetworkDiagnosticStatus.OK

    @property
    def has_warnings(self) -> bool:
        return self.warning_count > 0

    @property
    def has_errors(self) -> bool:
        return self.error_count > 0

    @property
    def has_insufficient_pressure(self) -> bool:
        return (
            self.status
            is DomesticWaterNetworkDiagnosticStatus.INSUFFICIENT_PRESSURE
        )

    @property
    def is_computed(self) -> bool:
        return self.status is not DomesticWaterNetworkDiagnosticStatus.NOT_COMPUTED


def build_domestic_water_network_diagnostic(
    compute_result: DomesticWaterNetworkComputeResult | None,
) -> DomesticWaterNetworkDiagnostic:
    """Build a consolidated diagnostic from a domestic water compute result."""

    if compute_result is None:
        return DomesticWaterNetworkDiagnostic(
            status=DomesticWaterNetworkDiagnosticStatus.NOT_COMPUTED,
            side=None,
        )

    messages = tuple(compute_result.messages)
    warning_count = sum(1 for message in messages if message.is_warning)
    error_count = sum(1 for message in messages if message.is_error)

    pressure_summary = compute_result.pressure_summary
    pressure_status = pressure_summary.status if pressure_summary else None
    critical_node_id = pressure_summary.critical_node_id if pressure_summary else None
    worst_pressure_bar = pressure_summary.worst_pressure_bar if pressure_summary else None
    pressure_margin_bar = (
        pressure_summary.pressure_margin_bar if pressure_summary else None
    )

    return DomesticWaterNetworkDiagnostic(
        status=_resolve_network_diagnostic_status(
            error_count=error_count,
            warning_count=warning_count,
            pressure_status=pressure_status,
        ),
        side=compute_result.side,
        section_count=compute_result.section_count,
        sized_section_count=compute_result.sized_section_count,
        pressure_loss_section_count=compute_result.pressure_loss_section_count,
        warning_count=warning_count,
        error_count=error_count,
        pressure_status=pressure_status,
        critical_node_id=critical_node_id,
        worst_pressure_bar=worst_pressure_bar,
        pressure_margin_bar=pressure_margin_bar,
        messages=messages,
    )


def _resolve_network_diagnostic_status(
    *,
    error_count: int,
    warning_count: int,
    pressure_status: PressureSummaryStatus | None,
) -> DomesticWaterNetworkDiagnosticStatus:
    if error_count > 0:
        return DomesticWaterNetworkDiagnosticStatus.ERRORS

    if pressure_status is PressureSummaryStatus.INSUFFICIENT_PRESSURE:
        return DomesticWaterNetworkDiagnosticStatus.INSUFFICIENT_PRESSURE

    if warning_count > 0:
        return DomesticWaterNetworkDiagnosticStatus.WARNINGS

    return DomesticWaterNetworkDiagnosticStatus.OK