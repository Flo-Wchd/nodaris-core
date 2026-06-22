from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.domain.fluids import FluidKind


def test_fluid_catalog_from_mapping() -> None:
    result = FluidCatalog.from_mapping(
        {
            "water_atm": [
                {
                    "temperature_c": 10,
                    "density_kg_m3": 999.77,
                    "dynamic_viscosity_pa_s": 0.001308,
                },
                {
                    "temperature_c": 60,
                    "density_kg_m3": 983.13,
                    "dynamic_viscosity_pa_s": 0.000467,
                },
                {
                    "temperature_c": 70,
                    "density_kg_m3": 977.76,
                    "dynamic_viscosity_pa_s": 0.000404,
                },
            ]
        }
    )

    assert result.ok
    assert result.value is not None

    catalog = result.value
    cold_water = catalog.get("cold_water")
    hot_water = catalog.get("hot_water")

    assert cold_water is not None
    assert cold_water.kind is FluidKind.COLD_WATER
    assert cold_water.temperature_c == 10
    assert cold_water.density_kg_m3 == 999.77

    assert hot_water is not None
    assert hot_water.kind is FluidKind.HOT_WATER
    assert hot_water.temperature_c == 60


def test_fluid_catalog_interpolates_water_temperature() -> None:
    result = FluidCatalog.from_mapping(
        {
            "water_atm": [
                {
                    "temperature_c": 10,
                    "density_kg_m3": 1000,
                    "dynamic_viscosity_pa_s": 0.001,
                },
                {
                    "temperature_c": 20,
                    "density_kg_m3": 990,
                    "dynamic_viscosity_pa_s": 0.0008,
                },
            ]
        }
    )

    assert result.value is not None

    fluid = result.value.get_water_at_temperature(15)

    assert fluid is not None
    assert fluid.temperature_c == 15
    assert fluid.density_kg_m3 == 995
    assert fluid.dynamic_viscosity_pa_s == 0.0009


def test_fluid_catalog_invalid_table_returns_failure() -> None:
    result = FluidCatalog.from_mapping({"water_atm": {}})

    assert result.failed
    assert result.errors[0].code == "WATER_ATM_TABLE_INVALID"