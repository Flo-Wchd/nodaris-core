from pathlib import Path

from ndc_core.catalogs.loaders.catalog_paths import (
    appliances_path,
    data_dir,
    find_project_root,
    pipes_path,
    singular_losses_cold_water_path,
    singular_losses_hot_water_path,
    standards_dir,
    water_atm_table_path,
)


def test_find_project_root_from_nested_directory(tmp_path: Path) -> None:
    root = tmp_path / "project"
    nested = root / "a" / "b"
    nested.mkdir(parents=True)
    (root / "pyproject.toml").write_text("[project]\nname = 'test'\n", encoding="utf-8")

    assert find_project_root(nested) == root


def test_catalog_paths_from_project_root(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()

    assert data_dir(root) == root / "data"
    assert standards_dir(root) == root / "data" / "standards"
    assert appliances_path(root) == root / "data" / "appliances.yaml"
    assert pipes_path(root) == root / "data" / "pipes.yaml"
    assert singular_losses_cold_water_path(root) == root / "data" / "singular_losses_cold_water.yaml"
    assert singular_losses_hot_water_path(root) == root / "data" / "singular_losses_hot_water.yaml"
    assert water_atm_table_path(root) == root / "data" / "water_atm_table.yaml"