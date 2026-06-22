from __future__ import annotations

from math import pi, sqrt

from ndc_core.hydraulics.conversions import diameter_mm_to_m, flow_l_s_to_m3_s


def circular_area_m2(diameter_m: float) -> float:
    """Return the internal area of a circular pipe."""

    try:
        diameter = float(diameter_m)
    except (TypeError, ValueError):
        return 0.0

    if diameter <= 0.0:
        return 0.0

    return pi * diameter**2 / 4.0


def velocity_m_s(flow_m3_s: float, internal_diameter_m: float) -> float:
    """Return mean velocity from flow and internal diameter in SI units."""

    try:
        flow = float(flow_m3_s)
        diameter = float(internal_diameter_m)
    except (TypeError, ValueError):
        return 0.0

    area = circular_area_m2(diameter)
    if flow <= 0.0 or area <= 0.0:
        return 0.0

    return flow / area


def velocity_from_l_s_and_mm(
    flow_l_s: float,
    internal_diameter_mm: float,
) -> float:
    """Return mean velocity from flow in L/s and internal diameter in mm."""

    return velocity_m_s(
        flow_m3_s=flow_l_s_to_m3_s(flow_l_s),
        internal_diameter_m=diameter_mm_to_m(internal_diameter_mm),
    )


def theoretical_diameter_m_for_velocity(
    flow_m3_s: float,
    target_velocity_m_s: float,
) -> float:
    """Return theoretical internal diameter for a target velocity."""

    try:
        flow = float(flow_m3_s)
        velocity = float(target_velocity_m_s)
    except (TypeError, ValueError):
        return 0.0

    if flow <= 0.0 or velocity <= 0.0:
        return 0.0

    return sqrt(4.0 * flow / (pi * velocity))


def theoretical_diameter_mm_for_velocity(
    flow_l_s: float,
    target_velocity_m_s: float,
) -> float:
    """Return theoretical internal diameter in mm from flow in L/s."""

    return theoretical_diameter_m_for_velocity(
        flow_m3_s=flow_l_s_to_m3_s(flow_l_s),
        target_velocity_m_s=target_velocity_m_s,
    ) * 1000.0