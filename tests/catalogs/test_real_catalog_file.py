from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.catalogs.singular_loss_catalog import SingularLossCatalog


def test_real_appliance_catalog_file_loads() -> None:
    result = ApplianceCatalog.from_yaml_file()

    assert result.ok
    assert result.value is not None
    assert result.value.list_codes()


def test_real_pipe_catalog_file_loads() -> None:
    result = PipeCatalog.from_yaml_file()

    assert result.ok
    assert result.value is not None
    assert result.value.list_material_codes()
    assert result.value.list_size_codes()


def test_real_singular_loss_catalog_file_loads() -> None:
    result = SingularLossCatalog.from_yaml_file()

    assert result.ok
    assert result.value is not None
    assert result.value.list_codes()


def test_real_fluid_catalog_file_loads() -> None:
    result = FluidCatalog.from_yaml_file()

    assert result.ok
    assert result.value is not None

    cold_water = result.value.get("cold_water")
    hot_water = result.value.get("hot_water")

    assert cold_water is not None
    assert hot_water is not None
    assert result.value.get_water_at_temperature(10.0) is not None