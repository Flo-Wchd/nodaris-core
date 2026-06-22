from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class FluidKind(StrEnum):
    """Supported fluid kinds."""

    COLD_WATER = "cold_water"
    HOT_WATER = "hot_water"
    HEATING_WATER = "heating_water"
    AIR = "air"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class Fluid:
    """
    Fluid physical properties.

    Values are deliberately explicit and SI-based to avoid hidden unit
    conversions inside the calculation engines.
    """

    code: str
    name: str
    kind: FluidKind = FluidKind.OTHER
    temperature_c: float = 10.0
    density_kg_m3: float = 1000.0
    dynamic_viscosity_pa_s: float = 0.001

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", self.code.strip())
        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "density_kg_m3", max(0.0, self.density_kg_m3))
        object.__setattr__(self, "dynamic_viscosity_pa_s", max(0.0, self.dynamic_viscosity_pa_s))

    @property
    def kinematic_viscosity_m2_s(self) -> float:
        if self.density_kg_m3 <= 0.0:
            return 0.0

        return self.dynamic_viscosity_pa_s / self.density_kg_m3