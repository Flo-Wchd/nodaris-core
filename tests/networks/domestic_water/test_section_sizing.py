from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.domain.appliances import Appliance
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import SectionUsageContext
from ndc_core.domain.pipes import PipeMaterial, PipeSize
from ndc_core.networks.domestic_water.section_sizing import (
    SectionSizingMode,
    size_cold_water_section_from_counts,
    size_hot_water_section_from_counts,
    velocity_limit_for_context,
)


def _appliance_catalog() -> ApplianceCatalog:
    return ApplianceCatalog(
        appliances_by_code={
            "L": Appliance(
                code="L",
                name="Lavabo",
                cold_water_flow_l_s=0.20,
                hot_water_flow_l_s=0.20,
                min_internal_diameter_mm=10.0,
            ),
            "D": Appliance(
                code="D",
                name="Douche",
                cold_water_flow_l_s=0.20,
                hot_water_flow_l_s=0.20,
                min_internal_diameter_mm=12.0,
            ),
            "WC": Appliance(
                code="WC",
                name="WC",
                cold_water_flow_l_s=0.12,
                hot_water_flow_l_s=0.0,
                min_internal_diameter_mm=10.0,
            ),
            "LL": Appliance(
                code="LL",
                name="Lave-linge",
                cold_water_flow_l_s=0.20,
                hot_water_flow_l_s=0.0,
                min_internal_diameter_mm=10.0,
            ),
            "LV": Appliance(
                code="LV",
                name="Lave-vaisselle",
                cold_water_flow_l_s=0.10,
                hot_water_flow_l_s=0.0,
                min_internal_diameter_mm=10.0,
            ),
        }
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


def test_velocity_limit_for_context() -> None:
    assert velocity_limit_for_context(SectionUsageContext.RISER) == 1.5
    assert velocity_limit_for_context(SectionUsageContext.BASEMENT) == 2.0
    assert velocity_limit_for_context(None) == 2.0


def test_size_cold_water_section_automatic() -> None:
    section = _section()

    result = size_cold_water_section_from_counts(
        section=section,
        appliance_counts={"L": 1, "D": 1, "WC": 1},
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
    )

    assert result.ok
    assert result.value is not None

    sizing = result.value

    assert sizing.mode is SectionSizingMode.AUTOMATIC
    assert sizing.demand.design_flow_l_s == 0.52
    assert sizing.selected_pipe_size is not None
    assert sizing.used_internal_diameter_mm is not None
    assert sizing.min_required_internal_diameter_mm == 12.0
    assert sizing.velocity_m_s is not None

    assert section.flow_l_s == sizing.demand.design_flow_l_s
    assert section.velocity_m_s == sizing.velocity_m_s
    assert section.selected_pipe_size_code == sizing.selected_pipe_size_code
    assert section.selected_internal_diameter_mm == sizing.used_internal_diameter_mm
    assert section.downstream_appliance_counts == {"L": 1, "D": 1, "WC": 1}
    assert section.effective_appliance_counts == {"L": 1, "D": 1, "WC": 1}


def test_size_section_respects_machine_exclusivity() -> None:
    section = _section()

    result = size_cold_water_section_from_counts(
        section=section,
        appliance_counts={"LL": 1, "LV": 1, "L": 1},
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
    )

    assert result.ok
    assert result.value is not None

    sizing = result.value

    assert sizing.demand.declared_appliance_count == 3
    assert sizing.demand.effective_appliance_count == 2
    assert section.downstream_appliance_counts == {
        "LL": 1,
        "LV": 1,
        "L": 1,
    }
    assert section.effective_appliance_counts in (
        {"LL": 1, "L": 1},
        {"LV": 1, "L": 1},
    )


def test_size_cold_water_section_with_forced_pipe() -> None:
    section = _section(forced_pipe_size_code="P20")

    result = size_cold_water_section_from_counts(
        section=section,
        appliance_counts={"L": 1},
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
    )

    assert result.ok
    assert result.value is not None

    sizing = result.value

    assert sizing.mode is SectionSizingMode.FORCED_PIPE
    assert sizing.selected_pipe_size_code == "P20"
    assert sizing.used_internal_diameter_mm == 20.0
    assert section.selected_pipe_size_code == "P20"
    assert section.selected_internal_diameter_mm == 20.0


def test_size_cold_water_section_with_forced_internal_diameter() -> None:
    section = _section(forced_internal_diameter_mm=18.0)

    result = size_cold_water_section_from_counts(
        section=section,
        appliance_counts={"L": 1},
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
    )

    assert result.ok
    assert result.value is not None

    sizing = result.value

    assert sizing.mode is SectionSizingMode.FORCED_INTERNAL_DIAMETER
    assert sizing.selected_pipe_size is None
    assert sizing.used_internal_diameter_mm == 18.0
    assert section.selected_pipe_size_code is None
    assert section.selected_internal_diameter_mm == 18.0


def test_forced_diameter_below_minimum_creates_warning() -> None:
    section = _section(forced_internal_diameter_mm=8.0)

    result = size_cold_water_section_from_counts(
        section=section,
        appliance_counts={"D": 1},
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
    )

    assert result.ok
    assert result.value is not None
    assert result.value.has_warnings
    assert any(
        message.code == "DOMESTIC_WATER_FORCED_DIAMETER_BELOW_MIN_DIAMETER"
        for message in result.value.messages
    )


def test_unknown_forced_pipe_returns_failure() -> None:
    section = _section(forced_pipe_size_code="UNKNOWN")

    result = size_cold_water_section_from_counts(
        section=section,
        appliance_counts={"L": 1},
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
    )

    assert result.failed
    assert result.value is not None
    assert result.value.has_errors
    assert any(
        message.code == "DOMESTIC_WATER_FORCED_PIPE_UNKNOWN"
        for message in result.value.messages
    )


def test_zero_hot_water_demand_returns_partial_without_exception() -> None:
    section = _section(fluid_code="ECS")

    result = size_hot_water_section_from_counts(
        section=section,
        appliance_counts={"WC": 1},
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
    )

    assert result.ok
    assert result.value is not None

    sizing = result.value

    assert not sizing.sized
    assert sizing.demand.design_flow_l_s == 0.0
    assert section.flow_l_s == 0.0
    assert section.selected_pipe_size_code is None
    assert section.selected_internal_diameter_mm is None
    assert any(
        message.code == "DOMESTIC_WATER_SECTION_NO_FLOW"
        for message in sizing.messages
    )