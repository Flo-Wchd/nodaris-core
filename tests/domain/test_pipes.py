from math import isclose, pi

from ndc_core.domain.pipes import PipeMaterial, PipeMaterialFamily, PipeSize


def test_pipe_material_normalizes_values() -> None:
    material = PipeMaterial(
        code=" copper ",
        name=" Cuivre ",
        family=PipeMaterialFamily.COPPER,
        default_roughness_m=-1.0,
    )

    assert material.code == "copper"
    assert material.name == "Cuivre"
    assert material.family is PipeMaterialFamily.COPPER
    assert material.default_roughness_m == 0.0


def test_pipe_size_normalizes_values() -> None:
    pipe_size = PipeSize(
        code=" cu_12x1 ",
        material_code=" copper ",
        nominal_diameter=" 12x1 ",
        internal_diameter_mm=10.0,
        external_diameter_mm=12.0,
        wall_thickness_mm=1.0,
    )

    assert pipe_size.code == "cu_12x1"
    assert pipe_size.material_code == "copper"
    assert pipe_size.nominal_diameter == "12x1"
    assert pipe_size.internal_diameter_mm == 10.0
    assert pipe_size.external_diameter_mm == 12.0
    assert pipe_size.wall_thickness_mm == 1.0


def test_pipe_size_internal_area() -> None:
    pipe_size = PipeSize(
        code="test",
        material_code="test",
        nominal_diameter="DN10",
        internal_diameter_mm=10.0,
    )

    assert pipe_size.internal_diameter_m == 0.01
    assert isclose(pipe_size.internal_area_m2, pi * 0.01**2 / 4.0)
    assert pipe_size.is_usable


def test_pipe_size_with_zero_internal_diameter_is_not_usable() -> None:
    pipe_size = PipeSize(
        code="invalid",
        material_code="test",
        nominal_diameter="invalid",
        internal_diameter_mm=-10.0,
    )

    assert pipe_size.internal_diameter_mm == 0.0
    assert pipe_size.internal_area_m2 == 0.0
    assert not pipe_size.is_usable