from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Appliance:
    """
    Sanitary appliance used as a demand source in a fluid network.

    This class is intentionally independent from YAML catalogs. Catalog loading,
    validation and alias management belong to ndc_core.catalogs.
    """

    code: str
    name: str
    cold_water_flow_l_s: float = 0.0
    hot_water_flow_l_s: float = 0.0
    min_internal_diameter_mm: float | None = None
    individual_coefficient: float | None = None
    load_units: float | None = None

    def __post_init__(self) -> None:
        normalized_code = self.code.strip()
        normalized_name = self.name.strip()

        object.__setattr__(self, "code", normalized_code)
        object.__setattr__(self, "name", normalized_name)
        object.__setattr__(self, "cold_water_flow_l_s", max(0.0, self.cold_water_flow_l_s))
        object.__setattr__(self, "hot_water_flow_l_s", max(0.0, self.hot_water_flow_l_s))

    @property
    def has_cold_water(self) -> bool:
        return self.cold_water_flow_l_s > 0.0

    @property
    def has_hot_water(self) -> bool:
        return self.hot_water_flow_l_s > 0.0

    @property
    def total_reference_flow_l_s(self) -> float:
        """
        Reference flow used when the appliance is treated globally.

        For mixed appliances, the cold and hot water flows are not added because
        they generally represent two possible supply sides of the same terminal.
        The most demanding side is retained.
        """

        return max(self.cold_water_flow_l_s, self.hot_water_flow_l_s)