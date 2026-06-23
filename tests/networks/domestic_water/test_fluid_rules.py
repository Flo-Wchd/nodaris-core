from __future__ import annotations

from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.domain.fluids import Fluid
from ndc_core.networks.domestic_water.fluid_rules import (
    default_domestic_water_fluid_code,
    resolve_domestic_water_fluid,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


def _fluid_catalog() -> FluidCatalog:
    cold = Fluid(
        code="cold_water",
        name="Cold water",
        temperature_c=10.0,
        density_kg_m3=1000.0,
        dynamic_viscosity_pa_s=0.001,
    )
    hot = Fluid(
        code="hot_water",
        name="Hot water",
        temperature_c=60.0,
        density_kg_m3=983.0,
        dynamic_viscosity_pa_s=0.000466,
    )

    return FluidCatalog(
        fluids_by_code={
            cold.code: cold,
            hot.code: hot,
        },
        water_points_by_temperature={
            10.0: cold,
            60.0: hot,
        },
    )


def test_default_domestic_water_fluid_code() -> None:
    assert default_domestic_water_fluid_code(DomesticWaterSide.COLD_WATER) == "cold_water"
    assert default_domestic_water_fluid_code(DomesticWaterSide.HOT_WATER) == "hot_water"


def test_resolve_domestic_water_fluid_uses_cold_default() -> None:
    messages: list[EngineMessage] = []

    fluid = resolve_domestic_water_fluid(
        fluid_catalog=_fluid_catalog(),
        side=DomesticWaterSide.COLD_WATER,
        water_temperature_c=None,
        messages=messages,
    )

    assert fluid is not None
    assert fluid.code == "cold_water"
    assert messages == []


def test_resolve_domestic_water_fluid_uses_hot_default() -> None:
    messages: list[EngineMessage] = []

    fluid = resolve_domestic_water_fluid(
        fluid_catalog=_fluid_catalog(),
        side=DomesticWaterSide.HOT_WATER,
        water_temperature_c=None,
        messages=messages,
    )

    assert fluid is not None
    assert fluid.code == "hot_water"
    assert messages == []


def test_resolve_domestic_water_fluid_temperature_override_has_priority() -> None:
    messages: list[EngineMessage] = []

    fluid = resolve_domestic_water_fluid(
        fluid_catalog=_fluid_catalog(),
        side=DomesticWaterSide.HOT_WATER,
        water_temperature_c=10.0,
        messages=messages,
    )

    assert fluid is not None
    assert fluid.code == "cold_water"
    assert fluid.temperature_c == 10.0
    assert messages == []


def test_resolve_domestic_water_fluid_unknown_temperature_adds_error() -> None:
    messages: list[EngineMessage] = []

    fluid = resolve_domestic_water_fluid(
        fluid_catalog=_fluid_catalog(),
        side=DomesticWaterSide.COLD_WATER,
        water_temperature_c=999.0,
        messages=messages,
    )

    assert fluid is None
    assert len(messages) == 1
    assert messages[0].is_error
    assert messages[0].code == "DOMESTIC_WATER_FLUID_TEMPERATURE_UNKNOWN"


def test_resolve_domestic_water_fluid_missing_default_adds_error() -> None:
    messages: list[EngineMessage] = []

    fluid = resolve_domestic_water_fluid(
        fluid_catalog=FluidCatalog(
            fluids_by_code={},
            water_points_by_temperature={},
        ),
        side=DomesticWaterSide.COLD_WATER,
        water_temperature_c=None,
        messages=messages,
    )

    assert fluid is None
    assert len(messages) == 1
    assert messages[0].is_error
    assert messages[0].code == "DOMESTIC_WATER_FLUID_MISSING"