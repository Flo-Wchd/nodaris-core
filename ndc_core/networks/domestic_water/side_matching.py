from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ndc_core.networks.domestic_water.types import DomesticWaterSide
from ndc_core.networks.domestic_water.entity_access import (
    read_downstream_section_ids,
)


_COLD_WATER_FLUID_CODES: tuple[str, ...] = (
    "efs",
    "cold_water",
    "domestic_cold_water",
)

_HOT_WATER_FLUID_CODES: tuple[str, ...] = (
    "ecs",
    "hot_water",
    "domestic_hot_water",
)


def normalize_domestic_water_fluid_code(value: Any) -> str:
    """
    Normalize a domestic water section fluid code.

    Accepted user-facing variants such as "cold water", "cold-water" and
    "cold_water" are normalized to the same canonical shape.
    """

    return (
        str(value or "")
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


def cold_water_fluid_codes() -> tuple[str, ...]:
    """Return canonical fluid codes accepted for EFS sections."""

    return _COLD_WATER_FLUID_CODES


def hot_water_fluid_codes() -> tuple[str, ...]:
    """Return canonical fluid codes accepted for ECS sections."""

    return _HOT_WATER_FLUID_CODES


def domestic_water_fluid_codes_for_side(
    side: DomesticWaterSide,
) -> tuple[str, ...]:
    """Return accepted fluid codes for the requested domestic water side."""

    if side is DomesticWaterSide.HOT_WATER:
        return hot_water_fluid_codes()

    return cold_water_fluid_codes()


def domestic_water_side_from_fluid_code(value: Any) -> DomesticWaterSide | None:
    """
    Resolve a domestic water side from a fluid code.

    Unknown codes return None instead of raising.
    """

    normalized = normalize_domestic_water_fluid_code(value)

    if normalized in cold_water_fluid_codes():
        return DomesticWaterSide.COLD_WATER

    if normalized in hot_water_fluid_codes():
        return DomesticWaterSide.HOT_WATER

    return None


def section_matches_domestic_water_side(
    section: Any,
    side: DomesticWaterSide,
) -> bool:
    """
    Return whether a section belongs to the requested domestic water side.
    """

    return (
        normalize_domestic_water_fluid_code(getattr(section, "fluid_code", None))
        in domestic_water_fluid_codes_for_side(side)
    )


def node_is_terminal_for_domestic_water_side(
    *,
    node: Any,
    sections: Mapping[str, Any],
    side: DomesticWaterSide,
) -> bool:
    """
    Return whether a node is terminal for the requested domestic water side.

    A node is terminal when it has no downstream section for that side.
    Downstream sections from other networks are ignored.
    """

    downstream_section_ids = read_downstream_section_ids(node)

    if not downstream_section_ids:
        return True

    for section_id in downstream_section_ids:
        section = sections.get(section_id)
        if section is not None and section_matches_domestic_water_side(section, side):
            return False

    return True