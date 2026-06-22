from __future__ import annotations

from math import log10, sqrt

from ndc_core.hydraulics.reynolds import flow_regime
from ndc_core.hydraulics.types import FlowRegime


def relative_roughness(roughness_m: float, internal_diameter_m: float) -> float:
    """Return relative roughness epsilon / D."""

    try:
        roughness = float(roughness_m)
        diameter = float(internal_diameter_m)
    except (TypeError, ValueError):
        return 0.0

    if roughness <= 0.0 or diameter <= 0.0:
        return 0.0

    return roughness / diameter


def laminar_friction_factor(reynolds: float) -> float:
    """Return Darcy friction factor in laminar regime."""

    try:
        re_value = float(reynolds)
    except (TypeError, ValueError):
        return 0.0

    if re_value <= 0.0:
        return 0.0

    return 64.0 / re_value


def swamee_jain_friction_factor(
    reynolds: float,
    relative_roughness_value: float,
) -> float:
    """Return explicit Swamee-Jain Darcy friction factor approximation."""

    try:
        re_value = float(reynolds)
        rr_value = max(0.0, float(relative_roughness_value))
    except (TypeError, ValueError):
        return 0.0

    if re_value <= 0.0:
        return 0.0

    try:
        return 0.25 / log10(rr_value / 3.7 + 5.74 / re_value**0.9) ** 2
    except (ValueError, ZeroDivisionError):
        return 0.0


def colebrook_white_friction_factor(
    reynolds: float,
    relative_roughness_value: float,
    *,
    max_iterations: int = 50,
    tolerance: float = 1e-8,
) -> float:
    """Return Darcy friction factor using fixed-point Colebrook-White solving."""

    try:
        re_value = float(reynolds)
        rr_value = max(0.0, float(relative_roughness_value))
    except (TypeError, ValueError):
        return 0.0

    if re_value <= 0.0:
        return 0.0

    factor = swamee_jain_friction_factor(re_value, rr_value) or 0.02

    for _ in range(max(1, int(max_iterations))):
        if factor <= 0.0:
            factor = 0.02

        try:
            inverse_sqrt = -2.0 * log10(
                rr_value / 3.7 + 2.51 / (re_value * sqrt(factor))
            )
            next_factor = 1.0 / inverse_sqrt**2
        except (ValueError, ZeroDivisionError):
            return factor

        if abs(next_factor - factor) <= tolerance:
            return next_factor

        factor = next_factor

    return factor


def darcy_friction_factor(
    reynolds: float,
    relative_roughness_value: float = 0.0,
) -> float:
    """Return Darcy friction factor for laminar, transition or turbulent flow."""

    regime = flow_regime(reynolds)

    if regime is FlowRegime.LAMINAR:
        return laminar_friction_factor(reynolds)

    turbulent_factor = colebrook_white_friction_factor(
        reynolds=reynolds,
        relative_roughness_value=relative_roughness_value,
    )

    if regime is FlowRegime.TURBULENT:
        return turbulent_factor

    laminar_at_limit = laminar_friction_factor(2300.0)
    turbulent_at_limit = colebrook_white_friction_factor(
        reynolds=4000.0,
        relative_roughness_value=relative_roughness_value,
    )

    try:
        alpha = (float(reynolds) - 2300.0) / (4000.0 - 2300.0)
    except (TypeError, ValueError):
        return 0.0

    return laminar_at_limit + alpha * (turbulent_at_limit - laminar_at_limit)