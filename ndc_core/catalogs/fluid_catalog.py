from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ndc_core.catalogs.loaders.catalog_paths import water_atm_table_path
from ndc_core.catalogs.loaders.yaml_loader import load_yaml_file
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.domain.fluids import Fluid, FluidKind


@dataclass(slots=True)
class FluidCatalog:
    """Catalog of fluids and water properties."""

    fluids_by_code: dict[str, Fluid] = field(default_factory=dict)
    water_points_by_temperature: dict[float, Fluid] = field(default_factory=dict)
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    def get(self, code: str) -> Fluid | None:
        normalized = code.strip()
        if not normalized:
            return None

        direct = self.fluids_by_code.get(normalized)
        if direct is not None:
            return direct

        lowered = normalized.lower()
        for raw_code, fluid in self.fluids_by_code.items():
            if raw_code.lower() == lowered:
                return fluid

        return None

    def get_water_at_temperature(self, temperature_c: float) -> Fluid | None:
        if not self.water_points_by_temperature:
            return None

        temperatures = sorted(self.water_points_by_temperature)

        if temperature_c <= temperatures[0]:
            return self.water_points_by_temperature[temperatures[0]]

        if temperature_c >= temperatures[-1]:
            return self.water_points_by_temperature[temperatures[-1]]

        for lower, upper in zip(temperatures[:-1], temperatures[1:]):
            if lower <= temperature_c <= upper:
                lower_fluid = self.water_points_by_temperature[lower]
                upper_fluid = self.water_points_by_temperature[upper]
                ratio = (temperature_c - lower) / (upper - lower)

                return Fluid(
                    code=f"water_{temperature_c:g}c",
                    name=f"Water at {temperature_c:g} °C",
                    kind=FluidKind.OTHER,
                    temperature_c=temperature_c,
                    density_kg_m3=_lerp(
                        lower_fluid.density_kg_m3,
                        upper_fluid.density_kg_m3,
                        ratio,
                    ),
                    dynamic_viscosity_pa_s=_lerp(
                        lower_fluid.dynamic_viscosity_pa_s,
                        upper_fluid.dynamic_viscosity_pa_s,
                        ratio,
                    ),
                )

        return self.water_points_by_temperature[temperatures[-1]]

    @classmethod
    def from_yaml_file(cls, path: Path | None = None) -> Result[FluidCatalog]:
        yaml_result = load_yaml_file(path or water_atm_table_path())
        if yaml_result.failed or yaml_result.value is None:
            return Result.failure(messages=yaml_result.messages)

        return cls.from_mapping(yaml_result.value, source=str(path or water_atm_table_path()))

    @classmethod
    def from_mapping(
        cls,
        data: dict[str, Any],
        *,
        source: str = "water_atm_table",
    ) -> Result[FluidCatalog]:
        messages: list[EngineMessage] = []
        points: dict[float, Fluid] = {}

        raw_points = data.get("water_atm", [])
        if not isinstance(raw_points, list):
            return Result.failure(
                messages=[
                    EngineMessage.error(
                        code="WATER_ATM_TABLE_INVALID",
                        text="water_atm must be a list.",
                        context={"source": source},
                    )
                ]
            )

        for raw_point in raw_points:
            if not isinstance(raw_point, dict):
                messages.append(
                    EngineMessage.warning(
                        code="WATER_ATM_POINT_INVALID",
                        text="Water ATM point must be a mapping.",
                        context={"source": source},
                    )
                )
                continue

            temperature = _to_optional_float(raw_point.get("temperature_c"))
            if temperature is None:
                messages.append(
                    EngineMessage.warning(
                        code="WATER_ATM_TEMPERATURE_MISSING",
                        text="Water ATM point temperature is missing.",
                        context={"source": source},
                    )
                )
                continue

            fluid = Fluid(
                code=f"water_{temperature:g}c",
                name=f"Water at {temperature:g} °C",
                kind=FluidKind.OTHER,
                temperature_c=temperature,
                density_kg_m3=_to_float(raw_point.get("density_kg_m3"), 1000.0),
                dynamic_viscosity_pa_s=_to_float(
                    raw_point.get("dynamic_viscosity_pa_s"),
                    0.001,
                ),
            )

            points[temperature] = fluid

        fluids = {
            "cold_water": cls._water_or_default(points, 10.0, FluidKind.COLD_WATER),
            "hot_water": cls._water_or_default(points, 60.0, FluidKind.HOT_WATER),
            "heating_water": cls._water_or_default(
                points,
                70.0,
                FluidKind.HEATING_WATER,
            ),
        }

        catalog = cls(
            fluids_by_code=fluids,
            water_points_by_temperature=points,
            messages=tuple(messages),
        )

        return Result.success(value=catalog, messages=messages)

    @staticmethod
    def _water_or_default(
        points: dict[float, Fluid],
        temperature_c: float,
        kind: FluidKind,
    ) -> Fluid:
        point = points.get(temperature_c)
        if point is None:
            return Fluid(
                code=kind.value,
                name=kind.value.replace("_", " ").title(),
                kind=kind,
                temperature_c=temperature_c,
            )

        return Fluid(
            code=kind.value,
            name=kind.value.replace("_", " ").title(),
            kind=kind,
            temperature_c=point.temperature_c,
            density_kg_m3=point.density_kg_m3,
            dynamic_viscosity_pa_s=point.dynamic_viscosity_pa_s,
        )


def _to_float(value: object, default: float = 0.0) -> float:
    if value is None:
        return default

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_optional_float(value: object) -> float | None:
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _lerp(lower: float, upper: float, ratio: float) -> float:
    return lower + ratio * (upper - lower)