from math import isclose, sqrt

from ndc_core.networks.domestic_water.simultaneity import (
    clamp_simultaneity_factor,
    collective_dtu_simultaneity_factor,
)


def test_collective_dtu_simultaneity_is_one_below_threshold() -> None:
    assert collective_dtu_simultaneity_factor(5, threshold=6) == 1.0


def test_collective_dtu_simultaneity_uses_formula_from_threshold() -> None:
    factor = collective_dtu_simultaneity_factor(6, threshold=6)

    assert isclose(factor, 0.8 / sqrt(5))


def test_collective_dtu_simultaneity_is_safe_for_invalid_values() -> None:
    assert collective_dtu_simultaneity_factor(0, threshold=6) == 1.0
    assert collective_dtu_simultaneity_factor(-1, threshold=6) == 1.0


def test_clamp_simultaneity_factor() -> None:
    assert clamp_simultaneity_factor(2.0) == 1.0
    assert clamp_simultaneity_factor(0.5) == 0.5
    assert clamp_simultaneity_factor(0.0) == 1.0