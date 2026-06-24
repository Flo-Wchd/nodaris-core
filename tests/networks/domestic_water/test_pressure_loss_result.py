from __future__ import annotations

from ndc_core.common.messages import EngineMessage
from ndc_core.domain.fluids import Fluid
from ndc_core.hydraulics.types import PressureLossBreakdown
from ndc_core.networks.domestic_water.pressure_loss_result import (
    DomesticWaterPressureLossResult,
    build_section_pressure_loss_result,
)
from ndc_core.networks.domestic_water.pressure_loss_types import (
    DomesticWaterPressureLossMode,
)
from ndc_core.networks.domestic_water.section_hydraulic_inputs import (
    DomesticWaterSectionHydraulicInputs,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


class _Section:
    id = "S1"
    velocity_m_s = None
    reynolds = None
    friction_factor = None
    linear_pressure_loss_pa = None
    singular_pressure_loss_pa = None
    elevation_pressure_loss_pa = None
    total_pressure_loss_pa = None
    singular_zeta_total = None


def _fluid() -> Fluid:
    return Fluid(
        code="cold_water",
        name="Cold water",
        temperature_c=10.0,
        density_kg_m3=1000.0,
        dynamic_viscosity_pa_s=0.001,
    )


def _inputs() -> DomesticWaterSectionHydraulicInputs:
    return DomesticWaterSectionHydraulicInputs(
        mode=DomesticWaterPressureLossMode.FULL,
        flow_l_s=0.2,
        internal_diameter_mm=20.0,
        internal_diameter_m=0.02,
        length_m=10.0,
        elevation_change_m=1.0,
        velocity_m_s=0.64,
    )


def _breakdown() -> PressureLossBreakdown:
    return PressureLossBreakdown(
        reynolds=12_345.0,
        friction_factor=0.021,
        linear_pressure_loss_pa=1_000.0,
        singular_pressure_loss_pa=250.0,
        elevation_pressure_change_pa=9_810.0,
        singular_zeta_total=2.0,
    )


def test_build_section_pressure_loss_result_success_writes_section_state() -> None:
    section = _Section()

    result = build_section_pressure_loss_result(
        section=section,
        side=DomesticWaterSide.COLD_WATER,
        fluid=_fluid(),
        inputs=_inputs(),
        breakdown=_breakdown(),
        relative_roughness_value=0.000075,
        messages=[],
    )

    assert result.ok
    assert result.value is not None
    assert isinstance(result.value, DomesticWaterPressureLossResult)

    pressure = result.value

    assert pressure.section_id == "S1"
    assert pressure.side is DomesticWaterSide.COLD_WATER
    assert pressure.mode is DomesticWaterPressureLossMode.FULL
    assert pressure.flow_l_s == 0.2
    assert pressure.internal_diameter_mm == 20.0
    assert pressure.length_m == 10.0
    assert pressure.velocity_m_s == 0.64
    assert pressure.relative_roughness_value == 0.000075

    assert section.velocity_m_s == 0.64
    assert section.reynolds == 12_345.0
    assert section.friction_factor == 0.021
    assert section.linear_pressure_loss_pa == 1_000.0
    assert section.singular_pressure_loss_pa == 250.0
    assert section.elevation_pressure_loss_pa == 9_810.0
    assert section.total_pressure_loss_pa == 11_060.0
    assert section.singular_zeta_total == 2.0


def test_build_section_pressure_loss_result_failure_when_messages_contain_error() -> None:
    section = _Section()
    message = EngineMessage.error(
        code="TEST_ERROR",
        text="Test error.",
        context={"section_id": "S1"},
    )

    result = build_section_pressure_loss_result(
        section=section,
        side=DomesticWaterSide.COLD_WATER,
        fluid=_fluid(),
        inputs=_inputs(),
        breakdown=_breakdown(),
        relative_roughness_value=0.000075,
        messages=[message],
    )

    assert result.failed
    assert result.value is not None
    assert result.value.has_errors
    assert result.messages == (message,)