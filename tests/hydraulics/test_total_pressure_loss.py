from ndc_core.hydraulics.total_pressure_loss import total_pressure_loss
from ndc_core.hydraulics.types import FlowRegime


def test_total_pressure_loss_breakdown() -> None:
    breakdown = total_pressure_loss(
        velocity_m_s=1.0,
        internal_diameter_m=0.02,
        length_m=10.0,
        density_kg_m3=1000.0,
        kinematic_viscosity_m2_s=1e-6,
        relative_roughness_value=0.0001,
        elevation_change_m=1.0,
        singular_zeta_values=[1.0, 2.0],
    )

    assert breakdown.reynolds == 20_000.0
    assert breakdown.flow_regime is FlowRegime.TURBULENT
    assert breakdown.friction_factor is not None
    assert breakdown.linear_pressure_loss_pa > 0.0
    assert breakdown.singular_zeta_total == 3.0
    assert breakdown.singular_pressure_loss_pa == 1500.0
    assert breakdown.elevation_pressure_change_pa == 9810.0
    assert breakdown.total_pressure_change_pa > 0.0


def test_total_pressure_loss_keeps_elevation_when_no_flow() -> None:
    breakdown = total_pressure_loss(
        velocity_m_s=0.0,
        internal_diameter_m=0.02,
        length_m=10.0,
        density_kg_m3=1000.0,
        kinematic_viscosity_m2_s=1e-6,
        elevation_change_m=-2.0,
        singular_zeta_values=[1.0],
    )

    assert breakdown.reynolds is None
    assert breakdown.linear_pressure_loss_pa == 0.0
    assert breakdown.singular_pressure_loss_pa == 0.0
    assert breakdown.elevation_pressure_change_pa == -19_620.0
    assert breakdown.total_pressure_change_pa == -19_620.0