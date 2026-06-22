from math import isclose

from ndc_core.hydraulics.friction import (
    darcy_friction_factor,
    laminar_friction_factor,
    relative_roughness,
)


def test_relative_roughness() -> None:
    assert isclose(relative_roughness(0.000001, 0.01), 0.0001)


def test_laminar_friction_factor() -> None:
    assert laminar_friction_factor(1000.0) == 0.064


def test_darcy_friction_factor_turbulent_returns_positive_value() -> None:
    factor = darcy_friction_factor(
        reynolds=100_000.0,
        relative_roughness_value=0.0001,
    )

    assert factor > 0.0
    assert isclose(factor, 0.0185, rel_tol=0.2)