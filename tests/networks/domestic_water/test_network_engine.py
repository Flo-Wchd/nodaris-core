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
from ndc_core.networks.domestic_water.network_engine import (
    DomesticWaterNetworkEngine,
    compute_cold_water_network,
)


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
            "WC": Appliance(
                code="WC",
                name="WC",
                cold_water_flow_l_s=0.12,
                hot_water_flow_l_s=0.0,
                min_internal_diameter_mm=10.0,
            ),
        }
    )


def _pipe_catalog() -> PipeCatalog:
    material = PipeMaterial(
        code="EFS",
        name="Test material",
        default_roughness_m=0.0000015,
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
            "P12": size_12,
            "P20": size_20,
        },
        size_codes_by_material={"EFS": ["P12", "P20"]},
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


def _section(
    section_id: str,
    downstream_node_id: str,
    *,
    counts: dict[str, int],
    elevation_change_m: float = 0.0,
) -> Section:
    section = Section(
        id=section_id,
        name=section_id,
        upstream_node_id="N0",
        downstream_node_id=downstream_node_id,
        fluid_code="EFS",
        usage_context=SectionUsageContext.RISER,
        length_m=10.0,
        elevation_change_m=elevation_change_m,
    )
    section.downstream_appliance_counts.update(counts)
    return section


def test_compute_sections_sizes_and_computes_pressure_losses() -> None:
    nodes = {
        "N0": _Node(id="N0", downstream_section_ids=["S1"]),
        "N1": _Node(id="N1", downstream_section_ids=[]),
    }
    sections = {
        "S1": _section(
            "S1",
            "N1",
            counts={"L": 1, "D": 1, "WC": 1},
        ),
    }

    engine = DomesticWaterNetworkEngine.cold_water(
        nodes=nodes,
        sections=sections,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    )

    result = engine.compute_sections()

    assert result.ok
    assert result.value is not None

    network_result = result.value

    assert network_result.section_count == 1
    assert network_result.sized_section_count == 1
    assert network_result.pressure_loss_section_count == 1

    section_result = network_result.section_results["S1"]

    assert section_result.sizing is not None
    assert section_result.pressure_loss is not None
    assert sections["S1"].selected_internal_diameter_mm is not None
    assert sections["S1"].velocity_m_s is not None
    assert sections["S1"].total_pressure_loss_pa is not None


def test_compute_all_sizes_losses_and_propagates_pressure() -> None:
    nodes = {
        "N0": _Node(id="N0", downstream_section_ids=["S1"]),
        "N1": _Node(id="N1", downstream_section_ids=[]),
    }
    sections = {
        "S1": _section(
            "S1",
            "N1",
            counts={"L": 1, "D": 1},
            elevation_change_m=0.0,
        ),
    }

    result = compute_cold_water_network(
        nodes=nodes,
        sections=sections,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
        source_node_id="N0",
        source_pressure_bar=3.0,
        min_required_pressure_bar=1.0,
    )

    assert result.ok
    assert result.value is not None

    network_result = result.value

    assert network_result.has_pressure_propagation
    assert network_result.has_pressure_summary
    assert network_result.pressure_propagation is not None
    assert network_result.pressure_summary is not None

    assert "N0" in network_result.pressure_propagation.node_pressures
    assert "N1" in network_result.pressure_propagation.node_pressures

    assert nodes["N0"].pressure_pa == 300_000.0
    assert nodes["N1"].pressure_pa is not None
    assert sections["S1"].pressure_start_pa == 300_000.0
    assert sections["S1"].pressure_end_pa is not None

    assert network_result.pressure_summary.worst_terminal is not None
    assert network_result.pressure_summary.worst_terminal.node_id == "N1"


def test_compute_all_without_source_only_computes_sections() -> None:
    nodes = {
        "N0": _Node(id="N0", downstream_section_ids=["S1"]),
        "N1": _Node(id="N1", downstream_section_ids=[]),
    }
    sections = {
        "S1": _section(
            "S1",
            "N1",
            counts={"L": 1},
        ),
    }

    result = compute_cold_water_network(
        nodes=nodes,
        sections=sections,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    )

    assert result.ok
    assert result.value is not None

    network_result = result.value

    assert network_result.section_count == 1
    assert not network_result.has_pressure_propagation
    assert not network_result.has_pressure_summary
    assert nodes["N0"].pressure_pa is None
    assert nodes["N1"].pressure_pa is None


def test_section_without_appliance_counts_returns_partial_without_exception() -> None:
    nodes = {
        "N0": _Node(id="N0", downstream_section_ids=["S1"]),
        "N1": _Node(id="N1", downstream_section_ids=[]),
    }
    sections = {
        "S1": _section(
            "S1",
            "N1",
            counts={},
        ),
    }

    result = compute_cold_water_network(
        nodes=nodes,
        sections=sections,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    )

    assert result.ok
    assert result.value is not None
    assert result.value.has_warnings
    assert result.value.section_results["S1"].sizing is not None
    assert result.value.section_results["S1"].pressure_loss is None

    assert any(
        message.code == "DOMESTIC_WATER_NETWORK_SECTION_NO_APPLIANCES"
        for message in result.value.messages
    )


def test_hot_water_engine_ignores_cold_water_sections() -> None:
    nodes = {
        "N0": _Node(id="N0", downstream_section_ids=["S1"]),
        "N1": _Node(id="N1", downstream_section_ids=[]),
    }
    sections = {
        "S1": _section(
            "S1",
            "N1",
            counts={"L": 1},
        ),
    }

    engine = DomesticWaterNetworkEngine.hot_water(
        nodes=nodes,
        sections=sections,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    )

    result = engine.compute_sections()

    assert result.ok
    assert result.value is not None
    assert result.value.section_count == 0
    assert sections["S1"].selected_internal_diameter_mm is None