from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result


def load_yaml_file(path: Path) -> Result[dict[str, Any]]:
    """
    Load a YAML file and return a managed Result.

    Normal runtime errors are converted into EngineMessage objects. The caller
    can decide whether a failure should stop a calculation or only block one
    catalog.
    """

    try:
        if not path.exists():
            return Result.failure(
                messages=[
                    EngineMessage.error(
                        code="YAML_FILE_NOT_FOUND",
                        text="YAML file was not found.",
                        context={"path": str(path)},
                    )
                ],
            )

        raw = path.read_text(encoding="utf-8")
        data = yaml.safe_load(raw)

    except yaml.YAMLError as exc:
        return Result.failure(
            messages=[
                EngineMessage.error(
                    code="YAML_PARSE_ERROR",
                    text="YAML file could not be parsed.",
                    context={"path": str(path), "error": str(exc)},
                )
            ],
        )

    except OSError as exc:
        return Result.failure(
            messages=[
                EngineMessage.error(
                    code="YAML_READ_ERROR",
                    text="YAML file could not be read.",
                    context={"path": str(path), "error": str(exc)},
                )
            ],
        )

    if data is None:
        return Result.success(value={})

    if not isinstance(data, dict):
        return Result.failure(
            messages=[
                EngineMessage.error(
                    code="YAML_ROOT_NOT_MAPPING",
                    text="YAML root must be a mapping.",
                    context={"path": str(path), "actual_type": type(data).__name__},
                )
            ],
        )

    return Result.success(value=data)


def require_mapping(
    data: dict[str, Any],
    key: str,
    *,
    source: str,
) -> Result[dict[str, Any]]:
    """Return a child mapping from an already loaded YAML root."""

    value = data.get(key)

    if value is None:
        return Result.failure(
            messages=[
                EngineMessage.error(
                    code="YAML_REQUIRED_MAPPING_MISSING",
                    text="Required YAML mapping is missing.",
                    context={"source": source, "key": key},
                )
            ],
        )

    if not isinstance(value, dict):
        return Result.failure(
            messages=[
                EngineMessage.error(
                    code="YAML_REQUIRED_MAPPING_INVALID",
                    text="Required YAML value must be a mapping.",
                    context={
                        "source": source,
                        "key": key,
                        "actual_type": type(value).__name__,
                    },
                )
            ],
        )

    return Result.success(value=value)


def optional_mapping(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if isinstance(value, dict):
        return value

    return {}


def optional_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if isinstance(value, list):
        return value

    return []