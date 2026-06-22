from __future__ import annotations

from math import sqrt


def collective_dtu_simultaneity_factor(
    appliance_count: int,
    *,
    threshold: int = 6,
) -> float:
    """
    Return DTU collective simultaneity factor.

    For x below the threshold, no simultaneity is applied.
    From the threshold, the formula is:

        y = 0.8 / sqrt(x - 1)
    """

    try:
        count = int(appliance_count)
        limit = int(threshold)
    except (TypeError, ValueError):
        return 1.0

    if count < limit:
        return 1.0

    if count <= 1:
        return 1.0

    return 0.8 / sqrt(count - 1)


def clamp_simultaneity_factor(value: float) -> float:
    """Keep a simultaneity factor in a safe range."""

    try:
        factor = float(value)
    except (TypeError, ValueError):
        return 1.0

    if factor <= 0.0:
        return 1.0

    return min(1.0, factor)