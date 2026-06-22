from __future__ import annotations


def linear_pressure_loss_pa(
    friction_factor: float,
    length_m: float,
    internal_diameter_m: float,
    velocity_m_s: float,
    density_kg_m3: float,
) -> float:
    """
    Return Darcy-Weisbach linear pressure loss in Pa.

    Formula:

        dp = f * (L / D) * rho * v² / 2
    """

    try:
        factor = float(friction_factor)
        length = float(length_m)
        diameter = float(internal_diameter_m)
        velocity = float(velocity_m_s)
        density = float(density_kg_m3)
    except (TypeError, ValueError):
        return 0.0

    if (
        factor <= 0.0
        or length <= 0.0
        or diameter <= 0.0
        or velocity <= 0.0
        or density <= 0.0
    ):
        return 0.0

    return factor * (length / diameter) * 0.5 * density * velocity**2