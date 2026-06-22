from __future__ import annotations

from pathlib import Path


def find_project_root(start: Path | None = None) -> Path:
    """
    Return the project root by walking upward from ``start``.

    The project root is identified by common repository markers. This helper is
    intentionally filesystem-based and does not import application modules.
    """

    current = (start or Path.cwd()).resolve()
    markers = ("pyproject.toml", ".git", "mkdocs.yml")

    for candidate in (current, *current.parents):
        if any((candidate / marker).exists() for marker in markers):
            return candidate

    return current


def data_dir(project_root: Path | None = None) -> Path:
    """Return the project data directory."""

    root = project_root or find_project_root()
    return root / "data"


def standards_dir(project_root: Path | None = None) -> Path:
    """Return the standards data directory."""

    return data_dir(project_root) / "standards"


def appliances_path(project_root: Path | None = None) -> Path:
    return data_dir(project_root) / "appliances.yaml"


def pipes_path(project_root: Path | None = None) -> Path:
    return data_dir(project_root) / "pipes.yaml"


def singular_losses_cold_water_path(project_root: Path | None = None) -> Path:
    return data_dir(project_root) / "singular_losses_cold_water.yaml"


def singular_losses_hot_water_path(project_root: Path | None = None) -> Path:
    return data_dir(project_root) / "singular_losses_hot_water.yaml"


def water_atm_table_path(project_root: Path | None = None) -> Path:
    return data_dir(project_root) / "water_atm_table.yaml"