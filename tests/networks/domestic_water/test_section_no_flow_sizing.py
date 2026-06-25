from __future__ import annotations

from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import SectionUsageContext
from ndc_core.networks.domestic_water.section_no_flow_sizing import (
    build_no_flow_section_sizing,
)
from ndc_core.networks.domestic_water.section_sizing_result import (
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
        "fluid_code": "ECS",
        "usage_context": SectionUsageContext.RISER,
        "length_m": 10.0,
    }
    values.update(kwargs)
    return Section(**values)


def _zero_flow_demand() -> DomesticWaterDemand:
    return DomesticWaterDemand(
        side=DomesticWaterSide.HOT_WATER,
        method=DomesticWaterMethod.COLLECTIVE_DTU,
        declared_appliance_count=1,
        effective_appliance_count=0,
        raw_flow_l_s=0.0,
        simultaneity_factor=1.0,
        design_flow_l_s=0.0,
        items=(
            ApplianceDemandItem(
                appliance_code="WC",
                appliance_name="WC",
                declared_count=1,
                effective_count=0,
                unit_flow_l_s=0.0,
                total_flow_l_s=0.0,
            ),
        ),
    )


def test_build_no_flow_section_sizing() -> None:
    messages = []

    sizing = build_no_flow_section_sizing(
        section=_section(),
        demand=_zero_flow_demand(),
        side=DomesticWaterSide.HOT_WATER,
        min_required_diameter_mm=0.0,
        max_velocity_m_s=1.5,
        messages=messages,
    )

    assert sizing.mode is SectionSizingMode.AUTOMATIC
    assert sizing.side is DomesticWaterSide.HOT_WATER
    assert not sizing.sized
    assert sizing.selected_pipe_size is None
    assert sizing.selected_pipe_size_code is None
    assert sizing.theoretical_internal_diameter_mm is None
    assert sizing.min_required_internal_diameter_mm is None
    assert sizing.used_internal_diameter_mm is None
    assert sizing.velocity_m_s is None
    assert sizing.max_velocity_m_s == 1.5
    assert sizing.velocity_ok is None
    assert sizing.has_warnings
    assert not sizing.has_errors
    assert any(
        message.code == "DOMESTIC_WATER_SECTION_NO_FLOW"
        for message in sizing.messages
    )
    assert messages == list(sizing.messages)


def test_build_no_flow_section_sizing_keeps_min_required_diameter() -> None:
    sizing = build_no_flow_section_sizing(
        section=_section(),
        demand=_zero_flow_demand(),
        side=DomesticWaterSide.HOT_WATER,
        min_required_diameter_mm=12.0,
        max_velocity_m_s=1.5,
        messages=[],
    )

    assert sizing.min_required_internal_diameter_mm == 12.0