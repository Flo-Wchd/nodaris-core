from __future__ import annotations

from math import isclose

from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import SectionUsageContext
from ndc_core.domain.pipes import PipeMaterial, PipeSize
from ndc_core.networks.domestic_water.pipe_rules import (
    relative_roughness_for_section,
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
    )
    section.selected_pipe_size_code = "P20"
    return section


def _pipe_catalog() -> PipeCatalog:
    material = PipeMaterial(
        code="EFS",
        name="Test material",
        default_roughness_m=0.0000015,
    )
    size = PipeSize(
        code="P20",
        material_code="EFS",
        nominal_diameter="DN20",
        internal_diameter_mm=20.0,
    )

    return PipeCatalog(
        materials_by_code={"EFS": material},
        sizes_by_code={"P20": size},
        size_codes_by_material={"EFS": ["P20"]},
    )


def test_relative_roughness_for_section() -> None:
    value = relative_roughness_for_section(
        section=_section(),
        pipe_catalog=_pipe_catalog(),
        internal_diameter_m=0.02,
    )

    assert isclose(value, 0.000075)


def test_relative_roughness_for_section_without_catalog_returns_zero() -> None:
    assert (
        relative_roughness_for_section(
            section=_section(),
            pipe_catalog=None,
            internal_diameter_m=0.02,
        )
        == 0.0
    )


def test_relative_roughness_for_section_without_selected_pipe_returns_zero() -> None:
    section = _section()
    section.selected_pipe_size_code = None

    assert (
        relative_roughness_for_section(
            section=section,
            pipe_catalog=_pipe_catalog(),
            internal_diameter_m=0.02,
        )
        == 0.0
    )


def test_relative_roughness_for_section_with_unknown_pipe_returns_zero() -> None:
    section = _section()
    section.selected_pipe_size_code = "UNKNOWN"

    assert (
        relative_roughness_for_section(
            section=section,
            pipe_catalog=_pipe_catalog(),
            internal_diameter_m=0.02,
        )
        == 0.0
    )


def test_relative_roughness_for_section_with_unknown_material_returns_zero() -> None:
    size = PipeSize(
        code="P20",
        material_code="UNKNOWN",
        nominal_diameter="DN20",
        internal_diameter_mm=20.0,
    )
    catalog = PipeCatalog(
        materials_by_code={},
        sizes_by_code={"P20": size},
        size_codes_by_material={"UNKNOWN": ["P20"]},
    )

    assert (
        relative_roughness_for_section(
            section=_section(),
            pipe_catalog=catalog,
            internal_diameter_m=0.02,
        )
        == 0.0
    )