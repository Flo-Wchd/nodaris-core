from __future__ import annotations

from ndc_core.hydraulics.types import FlowRegime


def reynolds_number(
    velocity_m_s: float,
    internal_diameter_m: float,
    *,
    kinematic_viscosity_m2_s: float | None = None,
    density_kg_m3: float | None = None,
    dynamic_viscosity_pa_s: float | None = None,
) -> float:
    """
    Return Reynolds number for internal pipe flow.

    If kinematic viscosity is not provided, density and dynamic viscosity are
    used to compute it.
    """

    try:
        velocity = float(velocity_m_s)
        diameter = float(internal_diameter_m)
    except (TypeError, ValueError):
        return 0.0

    if velocity <= 0.0 or diameter <= 0.0:
        return 0.0

    if kinematic_viscosity_m2_s is None:
        if density_kg_m3 is None or dynamic_viscosity_pa_s is None:
            return 0.0

        try:
            density = float(density_kg_m3)
            dynamic_viscosity = float(dynamic_viscosity_pa_s)
        except (TypeError, ValueError):
            return 0.0

        if density <= 0.0 or dynamic_viscosity <= 0.0:
            return 0.0

        kinematic_viscosity_m2_s = dynamic_viscosity / density

    try:
        kinematic_viscosity = float(kinematic_viscosity_m2_s)
    except (TypeError, ValueError):
        return 0.0

    if kinematic_viscosity <= 0.0:
        return 0.0

    return velocity * diameter / kinematic_viscosity


def flow_regime(
    reynolds: float,
    *,
    laminar_limit: float = 2300.0,
    turbulent_limit: float = 4000.0,
) -> FlowRegime:
    """Return qualitative flow regime."""

    try:
        re_value = float(reynolds)
    except (TypeError, ValueError):
        return FlowRegime.LAMINAR

    if re_value < laminar_limit:
        return FlowRegime.LAMINAR

    if re_value < turbulent_limit:
        return FlowRegime.TRANSITION

    return FlowRegime.TURBULENT