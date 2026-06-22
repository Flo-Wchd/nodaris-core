from __future__ import annotations

MM_PER_METER = 1000.0
LITERS_PER_CUBIC_METER = 1000.0
PASCALS_PER_BAR = 100_000.0


def flow_l_s_to_m3_s(flow_l_s: float) -> float:
    """Convert a flow from L/s to m³/s."""

    try:
        return float(flow_l_s) / LITERS_PER_CUBIC_METER
    except (TypeError, ValueError):
        return 0.0


def flow_m3_s_to_l_s(flow_m3_s: float) -> float:
    """Convert a flow from m³/s to L/s."""

    try:
        return float(flow_m3_s) * LITERS_PER_CUBIC_METER
    except (TypeError, ValueError):
        return 0.0


def diameter_mm_to_m(diameter_mm: float) -> float:
    """Convert a diameter from mm to m."""

    try:
        return float(diameter_mm) / MM_PER_METER
    except (TypeError, ValueError):
        return 0.0


def diameter_m_to_mm(diameter_m: float) -> float:
    """Convert a diameter from m to mm."""

    try:
        return float(diameter_m) * MM_PER_METER
    except (TypeError, ValueError):
        return 0.0


def pressure_bar_to_pa(pressure_bar: float) -> float:
    """Convert pressure from bar to Pa."""

    try:
        return float(pressure_bar) * PASCALS_PER_BAR
    except (TypeError, ValueError):
        return 0.0


def pressure_pa_to_bar(pressure_pa: float) -> float:
    """Convert pressure from Pa to bar."""

    try:
        return float(pressure_pa) / PASCALS_PER_BAR
    except (TypeError, ValueError):
        return 0.0