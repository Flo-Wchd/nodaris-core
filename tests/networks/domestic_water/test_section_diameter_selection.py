from __future__ import annotations

from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import SectionUsageContext
from ndc_core.domain.pipes import PipeMaterial, PipeSize
from ndc_core.networks.domestic_water.section_diameter_selection import (
    select_section_diameter,
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


def _pipe_catalog() -> PipeCatalog:
    material = PipeMaterial(
        code="EFS",
        name="Test pressure pipe",
    )
    size_10 = PipeSize(
        code="P10",
        material_code="EFS",
        nominal_diameter="DN10",
        internal_diameter_mm=10.0,
    )
    size_12 = PipeSize(
        code="P12",
        material_code="EFS",
        nominal_diameter="DN12",
        internal_diameter_mm=12.0,
    )
    size_20 = PipeSize(
        code="P20",
        material_code="EFS",
        nominal_diameter="DN20",
        internal_diameter_mm=20.0,
    )

    return PipeCatalog(
        materials_by_code={"EFS": material},
        sizes_by_code={
            size_10.code: size_10,
            size_12.code: size_12,
            size_20.code: size_20,
        },
        size_codes_by_material={
            "EFS": ["P10", "P12", "P20"],
        },
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


def _demand(flow_l_s: float = 0.52) -> DomesticWaterDemand:
    return DomesticWaterDemand(
        side=DomesticWaterSide.COLD_WATER,
        method=DomesticWaterMethod.COLLECTIVE_DTU,
        declared_appliance_count=3,
        effective_appliance_count=3,
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


def test_select_section_diameter_automatic() -> None:
    messages = []

    sizing = select_section_diameter(
        section=_section(),
        demand=_demand(),
        pipe_catalog=_pipe_catalog(),
        side=DomesticWaterSide.COLD_WATER,
        min_required_diameter_mm=12.0,
        max_velocity_m_s=2.0,
        messages=messages,
    )

    assert sizing.mode is SectionSizingMode.AUTOMATIC
    assert sizing.selected_pipe_size is not None
    assert sizing.used_internal_diameter_mm is not None
    assert sizing.min_required_internal_diameter_mm == 12.0
    assert not sizing.has_errors


def test_select_section_diameter_forced_pipe() -> None:
    messages = []

    sizing = select_section_diameter(
        section=_section(forced_pipe_size_code="P20"),
        demand=_demand(flow_l_s=0.20),
        pipe_catalog=_pipe_catalog(),
        side=DomesticWaterSide.COLD_WATER,
        min_required_diameter_mm=12.0,
        max_velocity_m_s=2.0,
        messages=messages,
    )

    assert sizing.mode is SectionSizingMode.FORCED_PIPE
    assert sizing.selected_pipe_size_code == "P20"
    assert sizing.used_internal_diameter_mm == 20.0
    assert not sizing.has_errors


def test_select_section_diameter_unknown_forced_pipe_adds_error() -> None:
    messages = []

    sizing = select_section_diameter(
        section=_section(forced_pipe_size_code="UNKNOWN"),
        demand=_demand(flow_l_s=0.20),
        pipe_catalog=_pipe_catalog(),
        side=DomesticWaterSide.COLD_WATER,
        min_required_diameter_mm=12.0,
        max_velocity_m_s=2.0,
        messages=messages,
    )

    assert sizing.mode is SectionSizingMode.FORCED_PIPE
    assert sizing.selected_pipe_size is None
    assert sizing.used_internal_diameter_mm is None
    assert sizing.has_errors
    assert any(
        message.code == "DOMESTIC_WATER_FORCED_PIPE_UNKNOWN"
        for message in sizing.messages
    )


def test_select_section_diameter_forced_internal_diameter() -> None:
    messages = []

    sizing = select_section_diameter(
        section=_section(forced_internal_diameter_mm=18.0),
        demand=_demand(flow_l_s=0.20),
        pipe_catalog=_pipe_catalog(),
        side=DomesticWaterSide.COLD_WATER,
        min_required_diameter_mm=12.0,
        max_velocity_m_s=2.0,
        messages=messages,
    )

    assert sizing.mode is SectionSizingMode.FORCED_INTERNAL_DIAMETER
    assert sizing.selected_pipe_size is None
    assert sizing.used_internal_diameter_mm == 18.0
    assert not sizing.has_errors


def test_select_section_diameter_forced_internal_diameter_below_minimum() -> None:
    messages = []

    sizing = select_section_diameter(
        section=_section(forced_internal_diameter_mm=8.0),
        demand=_demand(flow_l_s=0.20),
        pipe_catalog=_pipe_catalog(),
        side=DomesticWaterSide.COLD_WATER,
        min_required_diameter_mm=12.0,
        max_velocity_m_s=2.0,
        messages=messages,
    )

    assert sizing.mode is SectionSizingMode.FORCED_INTERNAL_DIAMETER
    assert sizing.has_warnings
    assert any(
        message.code == "DOMESTIC_WATER_FORCED_DIAMETER_BELOW_MIN_DIAMETER"
        for message in sizing.messages
    )