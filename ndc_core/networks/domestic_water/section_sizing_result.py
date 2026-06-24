from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from ndc_core.common.messages import EngineMessage
from ndc_core.domain.pipes import PipeSize
from ndc_core.networks.domestic_water.types import (
    DomesticWaterDemand,
    DomesticWaterSide,
)


class SectionSizingMode(StrEnum):
    """Section diameter selection mode."""

    AUTOMATIC = "automatic"
    FORCED_PIPE = "forced_pipe"
    FORCED_INTERNAL_DIAMETER = "forced_internal_diameter"


@dataclass(frozen=True, slots=True)
class DomesticWaterSectionSizing:
    """Sizing result for one domestic water section."""

    section_id: str
    side: DomesticWaterSide
    mode: SectionSizingMode
    demand: DomesticWaterDemand
    selected_pipe_size: PipeSize | None
    selected_pipe_size_code: str | None
    theoretical_internal_diameter_mm: float | None
    min_required_internal_diameter_mm: float | None
    used_internal_diameter_mm: float | None
    velocity_m_s: float | None
    max_velocity_m_s: float
    velocity_ok: bool | None
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @property
    def sized(self) -> bool:
        return self.used_internal_diameter_mm is not None

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)