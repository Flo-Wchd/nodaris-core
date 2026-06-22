from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import pi


class PipeMaterialFamily(StrEnum):
    """Main pipe material families used by the sizing engine."""

    COPPER = "copper"
    STAINLESS_STEEL = "stainless_steel"
    GALVANIZED_STEEL = "galvanized_steel"
    PEX = "pex"
    PB = "pb"
    PVC_C = "pvc_c"
    PPR = "ppr"
    MULTILAYER = "multilayer"
    CAST_IRON = "cast_iron"
    PVC = "pvc"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class PipeMaterial:
    """Pipe material definition."""

    code: str
    name: str
    family: PipeMaterialFamily = PipeMaterialFamily.OTHER
    default_roughness_m: float = 0.0001

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", self.code.strip())
        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "default_roughness_m", max(0.0, self.default_roughness_m))


@dataclass(frozen=True, slots=True)
class PipeSize:
    """
    Commercial pipe size.

    Diameters are expressed in millimetres because this is the most readable
    representation for building services design.
    """

    code: str
    material_code: str
    nominal_diameter: str
    internal_diameter_mm: float
    external_diameter_mm: float | None = None
    wall_thickness_mm: float | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", self.code.strip())
        object.__setattr__(self, "material_code", self.material_code.strip())
        object.__setattr__(self, "nominal_diameter", self.nominal_diameter.strip())
        object.__setattr__(self, "internal_diameter_mm", max(0.0, self.internal_diameter_mm))

        if self.external_diameter_mm is not None:
            object.__setattr__(self, "external_diameter_mm", max(0.0, self.external_diameter_mm))

        if self.wall_thickness_mm is not None:
            object.__setattr__(self, "wall_thickness_mm", max(0.0, self.wall_thickness_mm))

    @property
    def internal_diameter_m(self) -> float:
        return self.internal_diameter_mm / 1000.0

    @property
    def internal_area_m2(self) -> float:
        diameter_m = self.internal_diameter_m
        return pi * diameter_m**2 / 4.0

    @property
    def is_usable(self) -> bool:
        return self.internal_diameter_mm > 0.0 and self.internal_area_m2 > 0.0