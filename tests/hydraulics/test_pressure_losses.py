from math import isclose

from ndc_core.hydraulics.elevation_pressure_loss import (
    elevation_pressure_change_pa,
)
from ndc_core.hydraulics.linear_pressure_loss import linear_pressure_loss_pa
from ndc_core.hydraulics.singular_pressure_loss import (
    equivalent_zeta_from_kv,
    singular_pressure_loss_pa,
    sum_zeta,
)


def test_linear_pressure_loss_pa() -> None:
    pressure_loss = linear_pressure_loss_pa(
        friction_factor=0.02,
        length_m=10.0,
        internal_diameter_m=0.02,
        velocity_m_s=1.0,
        density_kg_m3=1000.0,
    )

    assert pressure_loss == 5000.0


def test_sum_zeta_ignores_invalid_values() -> None:
    assert sum_zeta([1.0, -1.0, None, 2.0]) == 3.0


def test_singular_pressure_loss_pa() -> None:
    pressure_loss = singular_pressure_loss_pa(
        zeta_total=2.0,
        velocity_m_s=1.0,
        density_kg_m3=1000.0,
    )

    assert pressure_loss == 1000.0


def test_equivalent_zeta_from_kv() -> None:
    zeta = equivalent_zeta_from_kv(
        flow_l_s=0.2,
        kv_m3_h=3.6,
        velocity_m_s=1.0,
        density_kg_m3=1000.0,
    )

    assert zeta > 0.0


def test_elevation_pressure_change_positive_when_downstream_is_higher() -> None:
    pressure_change = elevation_pressure_change_pa(
        elevation_change_m=10.0,
        density_kg_m3=1000.0,
    )

    assert isclose(pressure_change, 98_100.0)


def test_elevation_pressure_change_negative_when_downstream_is_lower() -> None:
    pressure_change = elevation_pressure_change_pa(
        elevation_change_m=-10.0,
        density_kg_m3=1000.0,
    )

    assert isclose(pressure_change, -98_100.0)