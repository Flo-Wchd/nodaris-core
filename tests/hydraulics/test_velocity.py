from math import isclose, pi

from ndc_core.hydraulics.velocity import (
    circular_area_m2,
    theoretical_diameter_mm_for_velocity,
    velocity_from_l_s_and_mm,
)


def test_circular_area_m2() -> None:
    assert isclose(circular_area_m2(0.01), pi * 0.01**2 / 4.0)


def test_velocity_from_l_s_and_mm() -> None:
    velocity = velocity_from_l_s_and_mm(
        flow_l_s=0.2,
        internal_diameter_mm=12.0,
    )

    expected = 0.0002 / (pi * 0.012**2 / 4.0)

    assert isclose(velocity, expected)


def test_theoretical_diameter_mm_for_velocity() -> None:
    diameter = theoretical_diameter_mm_for_velocity(
        flow_l_s=0.2,
        target_velocity_m_s=2.0,
    )

    assert diameter > 0.0