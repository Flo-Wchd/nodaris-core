from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.domain.pipes import PipeMaterialFamily


def test_pipe_catalog_from_mapping() -> None:
    result = PipeCatalog.from_mapping(
        {
            "pipe_families": [
                {
                    "id": "PVC_P_PN16",
                    "label": "PVC-U pression PN16",
                    "material": "pvc",
                    "design_defaults": {"roughness_mm": 0.0015},
                    "variants": [
                        {
                            "id": "PVC_P_PN16_20",
                            "nominal_dn": 20,
                            "outer_diameter_mm": 20,
                            "inner_diameter_mm": 17,
                            "thickness_mm": 1.5,
                        }
                    ],
                }
            ]
        }
    )

    assert result.ok
    assert result.value is not None

    catalog = result.value
    material = catalog.get_material("pvc")
    pipe_size = catalog.get_size("pvc_p_pn16_20")

    assert material is not None
    assert material.family is PipeMaterialFamily.PVC
    assert material.default_roughness_m == 0.0000015

    assert pipe_size is not None
    assert pipe_size.code == "PVC_P_PN16_20"
    assert pipe_size.material_code == "pvc"
    assert pipe_size.internal_diameter_mm == 17
    assert pipe_size.external_diameter_mm == 20
    assert pipe_size.wall_thickness_mm == 1.5


def test_pipe_catalog_invalid_families_returns_failure() -> None:
    result = PipeCatalog.from_mapping({"pipe_families": {}})

    assert result.failed
    assert result.errors[0].code == "PIPE_FAMILIES_INVALID"


def test_pipe_catalog_lists_sizes_for_material() -> None:
    result = PipeCatalog.from_mapping(
        {
            "pipe_families": [
                {
                    "id": "FAM",
                    "label": "Famille",
                    "material": "pvc",
                    "variants": [
                        {
                            "id": "SIZE_1",
                            "nominal_dn": 20,
                            "inner_diameter_mm": 17,
                        }
                    ],
                }
            ]
        }
    )

    assert result.value is not None
    assert [size.code for size in result.value.list_sizes_for_material("pvc")] == [
        "SIZE_1"
    ]