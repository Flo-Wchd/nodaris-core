from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from ndc_core.common.messages import EngineMessage


class DomesticWaterSide(StrEnum):
    """Domestic water supply side."""

    COLD_WATER = "cold_water"
    HOT_WATER = "hot_water"


class DomesticWaterMethod(StrEnum):
    """Demand computation method."""

    RAW_SUM = "raw_sum"
    COLLECTIVE_DTU = "collective_dtu"


@dataclass(frozen=True, slots=True)
class ApplianceDemandItem:
    """One appliance contribution before simultaneity."""

    appliance_code: str
    appliance_name: str
    declared_count: int
    effective_count: int
    unit_flow_l_s: float
    total_flow_l_s: float


@dataclass(frozen=True, slots=True)
class DomesticWaterDemand:
    """Theoretical domestic water demand result."""

    side: DomesticWaterSide
    method: DomesticWaterMethod
    declared_appliance_count: int
    effective_appliance_count: int
    raw_flow_l_s: float
    simultaneity_factor: float
    design_flow_l_s: float
    items: tuple[ApplianceDemandItem, ...] = field(default_factory=tuple)
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @property
    def has_flow(self) -> bool:
        return self.design_flow_l_s > 0.0

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)