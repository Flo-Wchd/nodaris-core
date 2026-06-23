from __future__ import annotations

from ndc_core.common.messages import EngineMessage
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import SectionUsageContext
from ndc_core.networks.domestic_water.pressure_loss_types import (
    DomesticWaterPressureLossMode,
)
from ndc_core.networks.domestic_water.section_hydraulic_inputs import (
    DomesticWaterSectionHydraulicInputs,
    prepare_section_hydraulic_inputs,
)


def _section() -> Section:
    section = Section(
        id="S1",
        name="Section 1",
        upstream_node_id="N1",
        downstream_node_id="N2",
        fluid_code="EFS",
        usage_context=SectionUsageContext.RISER,
        length_m=10.0,
        elevation_change_m=1.0,
    )
    section.flow_l_s = 0.2
    section.selected_internal_diameter_mm = 20.0
    return section


def test_prepare_section_hydraulic_inputs_full_mode() -> None:
    messages: list[EngineMessage] = []

    inputs = prepare_section_hydraulic_inputs(
        section=_section(),
        messages=messages,
    )

    assert isinstance(inputs, DomesticWaterSectionHydraulicInputs)
    assert inputs.mode is DomesticWaterPressureLossMode.FULL
    assert inputs.flow_l_s == 0.2
    assert inputs.internal_diameter_mm == 20.0
    assert inputs.internal_diameter_m == 0.02
    assert inputs.length_m == 10.0
    assert inputs.elevation_change_m == 1.0
    assert inputs.velocity_m_s > 0.0
    assert messages == []


def test_prepare_section_hydraulic_inputs_elevation_only_mode() -> None:
    section = _section()
    section.flow_l_s = 0.0
    messages: list[EngineMessage] = []

    inputs = prepare_section_hydraulic_inputs(
        section=section,
        messages=messages,
    )

    assert inputs is not None
    assert inputs.mode is DomesticWaterPressureLossMode.ELEVATION_ONLY
    assert inputs.flow_l_s == 0.0
    assert inputs.velocity_m_s == 0.0
    assert len(messages) == 1
    assert messages[0].code == "DOMESTIC_WATER_PRESSURE_ELEVATION_ONLY"


def test_prepare_section_hydraulic_inputs_missing_diameter_returns_none() -> None:
    section = _section()
    section.selected_internal_diameter_mm = None
    messages: list[EngineMessage] = []

    inputs = prepare_section_hydraulic_inputs(
        section=section,
        messages=messages,
    )

    assert inputs is None
    assert len(messages) == 1
    assert messages[0].is_error
    assert messages[0].code == "DOMESTIC_WATER_PRESSURE_DIAMETER_MISSING"


def test_prepare_section_hydraulic_inputs_clamps_negative_length() -> None:
    section = _section()
    section.length_m = -10.0
    messages: list[EngineMessage] = []

    inputs = prepare_section_hydraulic_inputs(
        section=section,
        messages=messages,
    )

    assert inputs is not None
    assert inputs.length_m == 0.0