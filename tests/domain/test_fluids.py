from ndc_core.domain.fluids import Fluid, FluidKind


def test_fluid_normalizes_values() -> None:
    fluid = Fluid(
        code=" cold_water ",
        name=" Eau froide ",
        kind=FluidKind.COLD_WATER,
        temperature_c=10.0,
        density_kg_m3=999.7,
        dynamic_viscosity_pa_s=0.0013,
    )

    assert fluid.code == "cold_water"
    assert fluid.name == "Eau froide"
    assert fluid.kind is FluidKind.COLD_WATER
    assert fluid.temperature_c == 10.0
    assert fluid.density_kg_m3 == 999.7
    assert fluid.dynamic_viscosity_pa_s == 0.0013


def test_fluid_negative_physical_values_are_clamped() -> None:
    fluid = Fluid(
        code="invalid",
        name="Invalid",
        density_kg_m3=-1.0,
        dynamic_viscosity_pa_s=-2.0,
    )

    assert fluid.density_kg_m3 == 0.0
    assert fluid.dynamic_viscosity_pa_s == 0.0
    assert fluid.kinematic_viscosity_m2_s == 0.0


def test_fluid_kinematic_viscosity() -> None:
    fluid = Fluid(
        code="water",
        name="Water",
        density_kg_m3=1000.0,
        dynamic_viscosity_pa_s=0.001,
    )

    assert fluid.kinematic_viscosity_m2_s == 0.000001