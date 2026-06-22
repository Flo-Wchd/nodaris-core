from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ndc_core.domain.pipes import PipeSize


class FlowRegime(StrEnum):
    """Hydraulic flow regime based on Reynolds number."""

    LAMINAR = "laminar"
    TRANSITION = "transition"
    TURBULENT = "turbulent"


@dataclass(frozen=True, slots=True)
class PressureLossBreakdown:
    """
    Pressure loss breakdown for one hydraulic section.

    Sign convention:
    - linear_pressure_loss_pa is always positive or zero.
    - singular_pressure_loss_pa is always positive or zero.
    - elevation_pressure_change_pa can be positive or negative.

    Total pressure change is:

        linear + singular + elevation

    Network propagation must later use:

        downstream_pressure = upstream_pressure - total_pressure_change
    """

    reynolds: float | None = None
    flow_regime: FlowRegime | None = None
    friction_factor: float | None = None
    linear_pressure_loss_pa: float = 0.0
    singular_pressure_loss_pa: float = 0.0
    elevation_pressure_change_pa: float = 0.0
    singular_zeta_total: float = 0.0

    @property
    def total_pressure_change_pa(self) -> float:
        return (
            self.linear_pressure_loss_pa
            + self.singular_pressure_loss_pa
            + self.elevation_pressure_change_pa
        )


@dataclass(frozen=True, slots=True)
class PipeSizingResult:
    """Result of a simple pipe selection by maximum velocity."""

    selected_pipe_size: PipeSize | None
    theoretical_internal_diameter_mm: float | None
    design_flow_l_s: float
    max_velocity_m_s: float
    real_velocity_m_s: float | None

    @property
    def found(self) -> bool:
        return self.selected_pipe_size is not None

    @property
    def velocity_ok(self) -> bool | None:
        if self.real_velocity_m_s is None:
            return None

        return self.real_velocity_m_s <= self.max_velocity_m_s