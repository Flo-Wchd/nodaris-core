from __future__ import annotations

from dataclasses import dataclass, field

from ndc_core.networks.domestic_water.types import DomesticWaterMethod, DomesticWaterSide


@dataclass(frozen=True, slots=True)
class DomesticWaterProfile:
    """
    Demand computation profile.

    This object centralizes rules that differ between EFS and ECS without
    hardcoding them inside the demand builder.
    """

    side: DomesticWaterSide
    method: DomesticWaterMethod = DomesticWaterMethod.COLLECTIVE_DTU
    simultaneity_threshold: int = 6
    machine_exclusive_codes: frozenset[str] = field(
        default_factory=lambda: frozenset({"LL", "LV"})
    )

    @property
    def flow_attribute_name(self) -> str:
        if self.side is DomesticWaterSide.COLD_WATER:
            return "cold_water_flow_l_s"

        return "hot_water_flow_l_s"


COLD_WATER_PROFILE = DomesticWaterProfile(side=DomesticWaterSide.COLD_WATER)
HOT_WATER_PROFILE = DomesticWaterProfile(side=DomesticWaterSide.HOT_WATER)