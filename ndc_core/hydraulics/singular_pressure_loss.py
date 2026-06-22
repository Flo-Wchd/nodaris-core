from __future__ import annotations

from collections.abc import Iterable


def sum_zeta(values: Iterable[float | int | None] | None) -> float:
    """Return positive zeta coefficients sum."""

    if values is None:
        return 0.0

    total = 0.0

    for value in values:
        try:
            zeta = float(value)
        except (TypeError, ValueError):
            continue

        if zeta > 0.0:
            total += zeta

    return total


def singular_pressure_loss_pa(
    zeta_total: float,
    velocity_m_s: float,
    density_kg_m3: float,
) -> float:
    """
    Return singular pressure loss in Pa.

    Formula:

        dp = zeta * rho * v² / 2
    """

    try:
        zeta = float(zeta_total)
        velocity = float(velocity_m_s)
        density = float(density_kg_m3)
    except (TypeError, ValueError):
        return 0.0

    if zeta <= 0.0 or velocity <= 0.0 or density <= 0.0:
        return 0.0

    return zeta * 0.5 * density * velocity**2


def equivalent_zeta_from_kv(
    flow_l_s: float,
    kv_m3_h: float,
    velocity_m_s: float,
    density_kg_m3: float,
) -> float:
    """
    Convert a Kv value to an equivalent zeta coefficient.

    Kv convention used here:
    - flow in m³/h
    - pressure drop in bar
    - water-relative density correction
    """

    try:
        flow = float(flow_l_s)
        kv = float(kv_m3_h)
        velocity = float(velocity_m_s)
        density = float(density_kg_m3)
    except (TypeError, ValueError):
        return 0.0

    if flow <= 0.0 or kv <= 0.0 or velocity <= 0.0 or density <= 0.0:
        return 0.0

    flow_m3_h = flow * 3.6
    density_ratio = density / 1000.0
    pressure_drop_bar = (flow_m3_h / kv) ** 2 * density_ratio
    pressure_drop_pa = pressure_drop_bar * 100_000.0

    dynamic_pressure_pa = 0.5 * density * velocity**2
    if dynamic_pressure_pa <= 0.0:
        return 0.0

    return pressure_drop_pa / dynamic_pressure_pa