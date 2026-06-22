from pathlib import Path

from ndc_core.catalogs.loaders.yaml_loader import (
    load_yaml_file,
    optional_list,
    optional_mapping,
    require_mapping,
)


def test_load_yaml_file_success(tmp_path: Path) -> None:
    path = tmp_path / "catalog.yaml"
    path.write_text(
        """
metadata:
  version: 1.0
items:
  A:
    name: Item A
""",
        encoding="utf-8",
    )

    result = load_yaml_file(path)

    assert result.ok
    assert result.value is not None
    assert result.value["metadata"]["version"] == 1.0
    assert result.value["items"]["A"]["name"] == "Item A"


def test_load_yaml_file_missing_file_returns_failure(tmp_path: Path) -> None:
    result = load_yaml_file(tmp_path / "missing.yaml")

    assert result.failed
    assert result.has_errors
    assert result.errors[0].code == "YAML_FILE_NOT_FOUND"


def test_load_yaml_file_invalid_yaml_returns_failure(tmp_path: Path) -> None:
    path = tmp_path / "invalid.yaml"
    path.write_text("invalid: [", encoding="utf-8")

    result = load_yaml_file(path)

    assert result.failed
    assert result.has_errors
    assert result.errors[0].code == "YAML_PARSE_ERROR"


def test_load_yaml_file_empty_yaml_returns_empty_dict(tmp_path: Path) -> None:
    path = tmp_path / "empty.yaml"
    path.write_text("", encoding="utf-8")

    result = load_yaml_file(path)

    assert result.ok
    assert result.value == {}


def test_load_yaml_file_non_mapping_root_returns_failure(tmp_path: Path) -> None:
    path = tmp_path / "list.yaml"
    path.write_text("- A\n- B\n", encoding="utf-8")

    result = load_yaml_file(path)

    assert result.failed
    assert result.errors[0].code == "YAML_ROOT_NOT_MAPPING"


def test_require_mapping_success() -> None:
    result = require_mapping(
        {"items": {"A": {"name": "Item A"}}},
        "items",
        source="test",
    )

    assert result.ok
    assert result.value == {"A": {"name": "Item A"}}


def test_require_mapping_missing_returns_failure() -> None:
    result = require_mapping({}, "items", source="test")

    assert result.failed
    assert result.errors[0].code == "YAML_REQUIRED_MAPPING_MISSING"


def test_require_mapping_invalid_returns_failure() -> None:
    result = require_mapping({"items": []}, "items", source="test")

    assert result.failed
    assert result.errors[0].code == "YAML_REQUIRED_MAPPING_INVALID"


def test_optional_helpers() -> None:
    data = {
        "mapping": {"A": 1},
        "list": [1, 2],
        "invalid_mapping": [],
        "invalid_list": {},
    }

    assert optional_mapping(data, "mapping") == {"A": 1}
    assert optional_mapping(data, "invalid_mapping") == {}
    assert optional_mapping(data, "missing") == {}

    assert optional_list(data, "list") == [1, 2]
    assert optional_list(data, "invalid_list") == []
    assert optional_list(data, "missing") == []