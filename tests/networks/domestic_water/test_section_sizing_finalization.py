from __future__ import annotations

from ndc_core.common.messages import EngineMessage
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import SectionUsageContext
from ndc_core.networks.domestic_water.section_sizing_context import (
    DomesticWaterSectionSizingContext,
)
from ndc_core.networks.domestic_water.section_sizing_finalization import (
    finalize_section_sizing_result,
)
from ndc_core.networks.domestic_water.section_sizing_result import (
    DomesticWaterSectionSizing,
    SectionSizingMode,
)
from ndc_core.networks.domestic_water.types import (
    ApplianceDemandItem,
    DomesticWaterDemand,
    DomesticWaterMethod,
    DomesticWaterSide,
)


def _section(**kwargs: object) -> Section:
    values = {
        "id": "S1",
        "name": "Section 1",
        "upstream_node_id": "N1",
        "downstream_node_id": "N2",
        "fluid_code": "EFS",
        "usage_context": SectionUsageContext.RISER,
        "length_m": 10.0,
    }
    values.update(kwargs)
    return Section(**values)


def _demand(flow_l_s: float = 0.20) -> DomesticWaterDemand:
    return DomesticWaterDemand(
        side=DomesticWaterSide.COLD_WATER,
        method=DomesticWaterMethod.COLLECTIVE_DTU,
        declared_appliance_count=1,
        effective_appliance_count=1,
        raw_flow_l_s=flow_l_s,
        simultaneity_factor=1.0,
        design_flow_l_s=flow_l_s,
        items=(
            ApplianceDemandItem(
                appliance_code="L",
                appliance_name="Lavabo",
                declared_count=1,
                effective_count=1,
                unit_flow_l_s=flow_l_s,
                total_flow_l_s=flow_l_s,
            ),
        ),
    )


def _context(
    *,
    messages: list[EngineMessage] | None = None,
) -> DomesticWaterSectionSizingContext:
    return DomesticWaterSectionSizingContext(
        demand=_demand(),
        raw_appliance_counts={"L": 1},
        effective_appliance_counts={"L": 1},
        min_required_diameter_mm=10.0,
        max_velocity_m_s=1.5,
        messages=messages or [],
    )


def _sizing(
    *,
    messages: tuple[EngineMessage, ...] = (),
    used_internal_diameter_mm: float | None = 20.0,
) -> DomesticWaterSectionSizing:
    return DomesticWaterSectionSizing(
        section_id="S1",
        side=DomesticWaterSide.COLD_WATER,
        mode=SectionSizingMode.AUTOMATIC,
        demand=_demand(),
        selected_pipe_size=None,
        selected_pipe_size_code="P20" if used_internal_diameter_mm else None,
        theoretical_internal_diameter_mm=18.0,
        min_required_internal_diameter_mm=10.0,
        used_internal_diameter_mm=used_internal_diameter_mm,
        velocity_m_s=0.64 if used_internal_diameter_mm else None,
        max_velocity_m_s=1.5,
        velocity_ok=True if used_internal_diameter_mm else None,
        messages=messages,
    )


def test_finalize_section_sizing_result_writes_section_state() -> None:
    section = _section()
    context = _context()
    sizing = _sizing()

    result = finalize_section_sizing_result(
        section=section,
        context=context,
        sizing=sizing,
    )

    assert result.ok
    assert result.value is sizing

    assert section.flow_l_s == sizing.demand.design_flow_l_s
    assert section.velocity_m_s == sizing.velocity_m_s
    assert section.selected_pipe_size_code == "P20"
    assert section.selected_internal_diameter_mm == 20.0
    assert section.downstream_appliance_counts == {"L": 1}
    assert section.effective_appliance_counts == {"L": 1}


def test_finalize_section_sizing_result_returns_partial_on_warning() -> None:
    warning = EngineMessage.warning(
        code="TEST_WARNING",
        text="Test warning.",
        context={"section_id": "S1"},
    )
    context = _context(messages=[warning])
    sizing = _sizing(messages=(warning,))

    result = finalize_section_sizing_result(
        section=_section(),
        context=context,
        sizing=sizing,
    )

    assert result.ok
    assert result.has_warnings
    assert result.value is sizing


def test_finalize_section_sizing_result_returns_failure_on_error() -> None:
    error = EngineMessage.error(
        code="TEST_ERROR",
        text="Test error.",
        context={"section_id": "S1"},
    )
    context = _context(messages=[error])
    sizing = _sizing(
        messages=(error,),
        used_internal_diameter_mm=None,
    )

    result = finalize_section_sizing_result(
        section=_section(),
        context=context,
        sizing=sizing,
    )

    assert result.failed
    assert result.has_errors
    assert result.value is sizing