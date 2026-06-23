from __future__ import annotations

from dataclasses import dataclass

from ndc_core.networks.domestic_water.side_matching import (
    cold_water_fluid_codes,
    domestic_water_fluid_codes_for_side,
    domestic_water_side_from_fluid_code,
    hot_water_fluid_codes,
    normalize_domestic_water_fluid_code,
    section_matches_domestic_water_side,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


@dataclass
class _Section:
    fluid_code: str


def test_normalize_domestic_water_fluid_code() -> None:
    assert normalize_domestic_water_fluid_code(" EFS ") == "efs"
    assert normalize_domestic_water_fluid_code("cold water") == "cold_water"
    assert normalize_domestic_water_fluid_code("cold-water") == "cold_water"
    assert normalize_domestic_water_fluid_code("domestic hot water") == "domestic_hot_water"
    assert normalize_domestic_water_fluid_code(None) == ""


def test_domestic_water_fluid_codes_are_canonical() -> None:
    assert cold_water_fluid_codes() == (
        "efs",
        "cold_water",
        "domestic_cold_water",
    )
    assert hot_water_fluid_codes() == (
        "ecs",
        "hot_water",
        "domestic_hot_water",
    )


def test_domestic_water_fluid_codes_for_side() -> None:
    assert domestic_water_fluid_codes_for_side(DomesticWaterSide.COLD_WATER) == (
        "efs",
        "cold_water",
        "domestic_cold_water",
    )
    assert domestic_water_fluid_codes_for_side(DomesticWaterSide.HOT_WATER) == (
        "ecs",
        "hot_water",
        "domestic_hot_water",
    )


def test_domestic_water_side_from_fluid_code() -> None:
    assert domestic_water_side_from_fluid_code("EFS") is DomesticWaterSide.COLD_WATER
    assert (
        domestic_water_side_from_fluid_code("domestic cold water")
        is DomesticWaterSide.COLD_WATER
    )

    assert domestic_water_side_from_fluid_code("ECS") is DomesticWaterSide.HOT_WATER
    assert (
        domestic_water_side_from_fluid_code("domestic-hot-water")
        is DomesticWaterSide.HOT_WATER
    )

    assert domestic_water_side_from_fluid_code("heating") is None
    assert domestic_water_side_from_fluid_code("") is None


def test_section_matches_domestic_water_side() -> None:
    cold_section = _Section(fluid_code="cold water")
    hot_section = _Section(fluid_code="domestic-hot-water")
    unknown_section = _Section(fluid_code="heating")

    assert section_matches_domestic_water_side(
        cold_section,
        DomesticWaterSide.COLD_WATER,
    )
    assert not section_matches_domestic_water_side(
        cold_section,
        DomesticWaterSide.HOT_WATER,
    )

    assert section_matches_domestic_water_side(
        hot_section,
        DomesticWaterSide.HOT_WATER,
    )
    assert not section_matches_domestic_water_side(
        hot_section,
        DomesticWaterSide.COLD_WATER,
    )

    assert not section_matches_domestic_water_side(
        unknown_section,
        DomesticWaterSide.COLD_WATER,
    )
    assert not section_matches_domestic_water_side(
        unknown_section,
        DomesticWaterSide.HOT_WATER,
    )