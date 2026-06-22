from __future__ import annotations

GRAVITY_M_S2 = 9.81


def elevation_pressure_change_pa(
    elevation_change_m: float,
    density_kg_m3: float,
    *,
    gravity_m_s2: float = GRAVITY_M_S2,
) -> float:
    """
    Return pressure change due to elevation.

    elevation_change_m = z_downstream - z_upstream.

    Positive value means pressure loss.
    Negative value means pressure gain.
    """

    try:
        elevation_change = float(elevation_change_m)
        density = float(density_kg_m3)
        gravity = float(gravity_m_s2)
    except (TypeError, ValueError):
        return 0.0

    if density <= 0.0 or gravity <= 0.0:
        return 0.0

    return density * gravity * elevation_change