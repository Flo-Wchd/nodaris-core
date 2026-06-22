from ndc_core.hydraulics.reynolds import flow_regime, reynolds_number
from ndc_core.hydraulics.types import FlowRegime


def test_reynolds_number_with_kinematic_viscosity() -> None:
    reynolds = reynolds_number(
        velocity_m_s=1.0,
        internal_diameter_m=0.02,
        kinematic_viscosity_m2_s=1e-6,
    )

    assert reynolds == 20_000.0


def test_reynolds_number_with_dynamic_viscosity() -> None:
    reynolds = reynolds_number(
        velocity_m_s=1.0,
        internal_diameter_m=0.02,
        density_kg_m3=1000.0,
        dynamic_viscosity_pa_s=0.001,
    )

    assert reynolds == 20_000.0


def test_flow_regime() -> None:
    assert flow_regime(1000.0) is FlowRegime.LAMINAR
    assert flow_regime(3000.0) is FlowRegime.TRANSITION
    assert flow_regime(10_000.0) is FlowRegime.TURBULENT