from __future__ import annotations

from types import SimpleNamespace

from ndc_core.common.messages import EngineMessage
from ndc_core.networks.domestic_water.section_sizing import (
    DomesticWaterSectionSizing as EngineDomesticWaterSectionSizing,
)
from ndc_core.networks.domestic_water.section_sizing import (
    SectionSizingMode as EngineSectionSizingMode,
)
from ndc_core.networks.domestic_water.section_sizing_result import (
    DomesticWaterSectionSizing,
    SectionSizingMode,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


def test_section_sizing_result_exports_are_kept_from_section_sizing() -> None:
    assert EngineDomesticWaterSectionSizing is DomesticWaterSectionSizing
    assert EngineSectionSizingMode is SectionSizingMode


def test_section_sizing_mode_values() -> None:
    assert SectionSizingMode.AUTOMATIC.value == "automatic"
    assert SectionSizingMode.FORCED_PIPE.value == "forced_pipe"
    assert (
        SectionSizingMode.FORCED_INTERNAL_DIAMETER.value
        == "forced_internal_diameter"
    )


def test_section_sizing_result_helpers_for_sized_section() -> None:
    warning = EngineMessage.warning(
        code="TEST_WARNING",
        text="Test warning.",
        context={"section_id": "S1"},
    )

    sizing = DomesticWaterSectionSizing(
        section_id="S1",
        side=DomesticWaterSide.COLD_WATER,
        mode=SectionSizingMode.AUTOMATIC,
        demand=SimpleNamespace(design_flow_l_s=0.52),
        selected_pipe_size=SimpleNamespace(code="P20"),
        selected_pipe_size_code="P20",
        theoretical_internal_diameter_mm=18.0,
        min_required_internal_diameter_mm=12.0,
        used_internal_diameter_mm=20.0,
        velocity_m_s=1.65,
        max_velocity_m_s=2.0,
        velocity_ok=True,
        messages=(warning,),
    )

    assert sizing.sized
    assert sizing.has_warnings
    assert not sizing.has_errors


def test_section_sizing_result_helpers_for_error() -> None:
    error = EngineMessage.error(
        code="TEST_ERROR",
        text="Test error.",
        context={"section_id": "S1"},
    )

    sizing = DomesticWaterSectionSizing(
        section_id="S1",
        side=DomesticWaterSide.COLD_WATER,
        mode=SectionSizingMode.FORCED_PIPE,
        demand=SimpleNamespace(design_flow_l_s=0.52),
        selected_pipe_size=None,
        selected_pipe_size_code=None,
        theoretical_internal_diameter_mm=18.0,
        min_required_internal_diameter_mm=12.0,
        used_internal_diameter_mm=None,
        velocity_m_s=None,
        max_velocity_m_s=2.0,
        velocity_ok=None,
        messages=(error,),
    )

    assert not sizing.sized
    assert not sizing.has_warnings
    assert sizing.has_errors