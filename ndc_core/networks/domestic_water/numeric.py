from __future__ import annotations

from math import isfinite
from typing import Any


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Convert a value to float.

    Invalid values return the provided default instead of raising.
    """

    try:
        number = float(value)
    except (TypeError, ValueError):
        return default

    return number if isfinite(number) else default


def safe_positive_float(value: Any) -> float | None:
    """
    Convert a value to a strictly positive float.

    Invalid, zero and negative values return None.
    """

    if value is None:
        return None

    number = safe_float(value, default=0.0)

    if number <= 0.0:
        return None

    return number


def positive_optional_float(value: Any) -> float | None:
    """
    Alias for optional strictly positive user inputs.

    This name is kept explicit for GUI/domain inputs such as forced diameters.
    """

    return safe_positive_float(value)


def safe_non_negative_float(value: Any, default: float = 0.0) -> float:
    """
    Convert a value to a non-negative float.

    Invalid values return the provided default. Negative finite values are
    clamped to zero.
    """

    number = safe_float(value, default=default)

    if number < 0.0:
        return 0.0

    return number


def safe_pressure_pa(value: Any) -> float:
    """
    Convert a pressure value in Pa to a safe non-negative pressure.

    Invalid, non-finite and negative values return 0 Pa.
    """

    return safe_non_negative_float(value, default=0.0)