from ndc_core.hydraulics.conversions import (
    diameter_m_to_mm,
    diameter_mm_to_m,
    flow_l_s_to_m3_s,
    flow_m3_s_to_l_s,
    pressure_bar_to_pa,
    pressure_pa_to_bar,
)


def test_flow_conversions() -> None:
    assert flow_l_s_to_m3_s(1.0) == 0.001
    assert flow_m3_s_to_l_s(0.001) == 1.0


def test_diameter_conversions() -> None:
    assert diameter_mm_to_m(20.0) == 0.02
    assert diameter_m_to_mm(0.02) == 20.0


def test_pressure_conversions() -> None:
    assert pressure_bar_to_pa(3.0) == 300_000.0
    assert pressure_pa_to_bar(300_000.0) == 3.0