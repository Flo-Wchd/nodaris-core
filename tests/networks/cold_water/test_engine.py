from __future__ import annotations

from dataclasses import dataclass, field

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.domain.appliances import Appliance
from ndc_core.domain.fluids import Fluid
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import SectionUsageContext
from ndc_core.domain.pipes import PipeMaterial, PipeSize
from ndc_core.networks.cold_water import (
    ColdWaterNetworkEngine,
    compute_cold_water_network,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


@dataclass
class _Node:
    id: str
    downstream_section_ids: list[str] = field(default_factory=list)
    pressure_pa: float | None = None


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
        }
    )


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


def _fluid_catalog() -> FluidCatalog:
    cold = Fluid(
        code="cold_water",
        name="Cold water",
        temperature_c=10.0,
        density_kg_m3=1000.0,
        dynamic_viscosity_pa_s=0.001,
    )
    hot = Fluid(
        code="hot_water",
        name="Hot water",
        temperature_c=60.0,
        density_kg_m3=983.0,
        dynamic_viscosity_pa_s=0.000466,
    )

    return FluidCatalog(
        fluids_by_code={
            "cold_water": cold,
            "hot_water": hot,
        },
        water_points_by_temperature={
            10.0: cold,
            60.0: hot,
        },
    )


def _network() -> tuple[dict[str, _Node], dict[str, Section]]:
    nodes = {
        "N0": _Node(id="N0", downstream_section_ids=["S1"]),
        "N1": _Node(id="N1", downstream_section_ids=[]),
    }
    section = Section(
        id="S1",
        name="S1",
        upstream_node_id="N0",
        downstream_node_id="N1",
        fluid_code="EFS",
        usage_context=SectionUsageContext.RISER,
        length_m=10.0,
    )
    section.downstream_appliance_counts.update({"L": 1, "D": 1})

    return nodes, {"S1": section}


def test_cold_water_facade_exposes_cold_water_side() -> None:
    nodes, sections = _network()

    engine = ColdWaterNetworkEngine(
        nodes=nodes,
        sections=sections,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    )

    assert engine.side is DomesticWaterSide.COLD_WATER
    assert engine.domestic_engine().side is DomesticWaterSide.COLD_WATER


def test_cold_water_facade_compute_sections() -> None:
    nodes, sections = _network()

    engine = ColdWaterNetworkEngine(
        nodes=nodes,
        sections=sections,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    )

    result = engine.compute_sections()

    assert result.ok
    assert result.value is not None
    assert result.value.section_count == 1
    assert result.value.sized_section_count == 1
    assert result.value.pressure_loss_section_count == 1
    assert sections["S1"].selected_internal_diameter_mm is not None
    assert sections["S1"].total_pressure_loss_pa is not None


def test_compute_cold_water_network_functional_entry_point() -> None:
    nodes, sections = _network()

    result = compute_cold_water_network(
        nodes=nodes,
        sections=sections,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
        source_node_id="N0",
        source_pressure_bar=3.0,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.has_pressure_propagation
    assert result.value.has_pressure_summary
    assert nodes["N0"].pressure_pa == 300_000.0
    assert nodes["N1"].pressure_pa is not None