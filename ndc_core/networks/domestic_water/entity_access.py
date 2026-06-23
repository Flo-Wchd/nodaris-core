from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ndc_core.networks.domestic_water.appliance_counts import (
    merge_appliance_counts,
    normalize_appliance_counts,
)


def clean_entity_id(value: Any) -> str:
    """Return a normalized non-optional entity id string."""

    return str(value or "").strip()


def clean_optional_code(value: Any) -> str | None:
    """Return a normalized optional code, or None when empty."""

    text = clean_entity_id(value)
    return text or None


def read_downstream_section_ids(node: Any) -> tuple[str, ...]:
    """Read downstream section ids from a Node-like object."""

    raw_ids = getattr(node, "downstream_section_ids", None) or []

    ids: list[str] = []
    for raw_id in raw_ids:
        section_id = clean_entity_id(raw_id)
        if section_id:
            ids.append(section_id)

    return tuple(ids)


def read_cell_appliance_counts(cell: Any) -> dict[str, int]:
    """Read normalized appliance counts from a Cell-like object."""

    if cell is None:
        return {}

    merged: dict[str, int] = {}

    for attr_name in ("appliance_counts", "appliances"):
        value = getattr(cell, attr_name, None)
        if isinstance(value, dict):
            merged = merge_appliance_counts(
                merged,
                normalize_appliance_counts(value),
            )

    return merged


def read_node_local_appliance_counts(node: Any) -> dict[str, int]:
    """Read normalized local appliance counts from a Node-like object."""

    if node is None:
        return {}

    local_counts_method = getattr(node, "local_appliance_counts", None)
    if callable(local_counts_method):
        try:
            return normalize_appliance_counts(local_counts_method())
        except (TypeError, ValueError):
            return {}

    merged: dict[str, int] = {}

    for attr_name in ("appliance_counts", "appliances"):
        value = getattr(node, attr_name, None)
        if isinstance(value, dict):
            merged = merge_appliance_counts(
                merged,
                normalize_appliance_counts(value),
            )

    cells = getattr(node, "cells", None)
    if isinstance(cells, (list, tuple)):
        for cell in cells:
            merged = merge_appliance_counts(
                merged,
                read_cell_appliance_counts(cell),
            )

    return merged


def write_section_downstream_appliance_counts(
    section: Any,
    counts: Mapping[str, int] | None,
) -> None:
    """Write normalized downstream appliance counts on a Section-like object."""

    _write_mapping_attribute(
        entity=section,
        attribute_name="downstream_appliance_counts",
        values=normalize_appliance_counts(counts),
    )


def write_node_downstream_appliance_counts(
    node: Any,
    counts: Mapping[str, int] | None,
) -> None:
    """Write normalized downstream appliance counts on a Node-like object."""

    _write_mapping_attribute(
        entity=node,
        attribute_name="downstream_appliance_counts",
        values=normalize_appliance_counts(counts),
    )


def apply_section_pressures(
    *,
    section: Any,
    pressure_start_pa: float,
    pressure_end_pa: float,
) -> None:
    """Write computed start/end pressures on a Section-like object."""

    try:
        section.pressure_start_pa = pressure_start_pa
        section.pressure_end_pa = pressure_end_pa
    except (AttributeError, TypeError):
        return


def apply_node_pressures(
    nodes: Mapping[str, Any],
    node_states: Mapping[str, Any],
) -> None:
    """Write computed pressures on Node-like objects."""

    for node_id, state in node_states.items():
        node = nodes.get(node_id)
        if node is None:
            continue

        pressure_pa = getattr(state, "pressure_pa", None)

        try:
            node.pressure_pa = pressure_pa
        except (AttributeError, TypeError):
            continue


def _write_mapping_attribute(
    *,
    entity: Any,
    attribute_name: str,
    values: Mapping[str, int],
) -> None:
    target = getattr(entity, attribute_name, None)

    if isinstance(target, dict):
        target.clear()
        target.update(values)
        return

    try:
        setattr(entity, attribute_name, dict(values))
    except (AttributeError, TypeError):
        return