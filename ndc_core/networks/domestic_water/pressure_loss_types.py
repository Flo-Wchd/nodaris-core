from __future__ import annotations

from enum import StrEnum


class DomesticWaterPressureLossMode(StrEnum):
    """Pressure loss calculation mode."""

    FULL = "full"
    ELEVATION_ONLY = "elevation_only"