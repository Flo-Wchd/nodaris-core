from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.domain.fluids import Fluid
from ndc_core.hydraulics.types import PressureLossBreakdown
from ndc_core.networks.domestic_water.pressure_loss_types import (
    DomesticWaterPressureLossMode,
)
from ndc_core.networks.domestic_water.section_hydraulic_inputs import (
    DomesticWaterSectionHydraulicInputs,
)
from ndc_core.networks.domestic_water.section_state import (
    apply_section_pressure_loss_state,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


@dataclass(frozen=True, slots=True)
class DomesticWaterPressureLossResult:
    """Pressure loss result for one domestic water section."""

    section_id: str
    side: DomesticWaterSide
    mode: DomesticWaterPressureLossMode
    fluid: Fluid
    breakdown: PressureLossBreakdown
    flow_l_s: float
    internal_diameter_mm: float | None
    length_m: float
    velocity_m_s: float
    relative_roughness_value: float
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @property
    def reynolds(self) -> float | None:
        return self.breakdown.reynolds

    @property
    def linear_pressure_loss_pa(self) -> float:
        return self.breakdown.linear_pressure_loss_pa

    @property
    def singular_pressure_loss_pa(self) -> float:
        return self.breakdown.singular_pressure_loss_pa

    @property
    def elevation_pressure_change_pa(self) -> float:
        return self.breakdown.elevation_pressure_change_pa

    @property
    def total_pressure_change_pa(self) -> float:
        return self.breakdown.total_pressure_change_pa

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)


def build_section_pressure_loss_result(
    *,
    section: Any,
    side: DomesticWaterSide,
    fluid: Fluid,
    inputs: DomesticWaterSectionHydraulicInputs,
    breakdown: PressureLossBreakdown,
    relative_roughness_value: float,
    messages: Sequence[EngineMessage],
) -> Result[DomesticWaterPressureLossResult]:
    """
    Build, write and wrap a domestic water section pressure-loss result.

    This function is the single place converting the computed pressure-loss
    breakdown into:
    - a typed result object;
    - written Section state;
    - a managed Result success/failure.
    """

    result = DomesticWaterPressureLossResult(
        section_id=section.id,
        side=side,
        mode=inputs.mode,
        fluid=fluid,
        breakdown=breakdown,
        flow_l_s=inputs.flow_l_s,
        internal_diameter_mm=inputs.internal_diameter_mm,
        length_m=inputs.length_m,
        velocity_m_s=inputs.velocity_m_s,
        relative_roughness_value=relative_roughness_value,
        messages=tuple(messages),
    )

    apply_section_pressure_loss_state(section=section, pressure_loss=result)

    if result.has_errors:
        return Result.failure(value=result, messages=messages)

    return Result.success(value=result, messages=messages)