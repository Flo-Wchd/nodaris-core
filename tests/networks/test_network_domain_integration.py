from __future__ import annotations

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.domain.appliances import Appliance
from ndc_core.domain.fluids import Fluid
from ndc_core.domain.networks.network import Network
from ndc_core.domain.networks.node import Node
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import NodeKind, SectionUsageContext
from ndc_core.domain.pipes import PipeMaterial, PipeSize
from ndc_core.networks import (
    ColdWaterNetworkEngine,
    HotWaterNetworkEngine,
    compute_cold_water_network_from_network,
    compute_hot_water_network_from_network,
)
from ndc_core.networks.domestic_water.network_engine import (
    DomesticWaterNetworkEngine,
    compute_cold_water_network_from_domain,
    compute_hot_water_network_from_domain,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


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
    efs_material = PipeMaterial(
        code="EFS",
        name="EFS material",
        default_roughness_m=0.0000015,
    )
    ecs_material = PipeMaterial(
        code="ECS",
        name="ECS material",
        default_roughness_m=0.0000015,
    )

    efs_size = PipeSize(
        code="EFS20",
        material_code="EFS",
        nominal_diameter="DN20",
        internal_diameter_mm=20.0,
    )
    ecs_size = PipeSize(
        code="ECS20",
        material_code="ECS",
        nominal_diameter="DN20",
        internal_diameter_mm=20.0,
    )

    return PipeCatalog(
        materials_by_code={
            "EFS": efs_material,
            "ECS": ecs_material,
        },
        sizes_by_code={
            "EFS20": efs_size,
            "ECS20": ecs_size,
        },
        size_codes_by_material={
            "EFS": ["EFS20"],
            "ECS": ["ECS20"],
        },
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


def _network(fluid_code: str) -> Network:
    network = Network(id="N", name="Test network")

    source = Node(
        id="N0",
        name="Source",
        kind=NodeKind.SOURCE,
    )
    terminal = Node(
        id="N1",
        name="Terminal",
        kind=NodeKind.TERMINAL,
    )

    section = Section(
        id="S1",
        name="S1",
        upstream_node_id="N0",
        downstream_node_id="N1",
        fluid_code=fluid_code,
        usage_context=SectionUsageContext.RISER,
        length_m=10.0,
    )
    section.downstream_appliance_counts.update({"L": 1, "D": 1, "WC": 1})

    network.add_node(source)
    network.add_node(terminal)
    network.add_section(section)

    return network


def test_domestic_water_engine_can_be_created_from_domain_network() -> None:
    network = _network("EFS")

    engine = DomesticWaterNetworkEngine.cold_water_from_network(
        network=network,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    )

    assert engine.side is DomesticWaterSide.COLD_WATER
    assert engine.nodes is network.nodes
    assert engine.sections is network.sections

    result = engine.compute_all(
        source_node_id="N0",
        source_pressure_bar=3.0,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.section_count == 1
    assert result.value.has_pressure_propagation
    assert network.get_node("N1") is not None
    assert network.get_node("N1").pressure_pa is not None


def test_cold_water_facade_from_network_computes_domain_network() -> None:
    network = _network("EFS")

    engine = ColdWaterNetworkEngine.from_network(
        network=network,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    )

    result = engine.compute_all(
        source_node_id="N0",
        source_pressure_bar=3.0,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.section_count == 1
    assert network.get_section("S1").selected_internal_diameter_mm is not None
    assert network.get_section("S1").total_pressure_loss_pa is not None
    assert network.get_node("N0").pressure_pa == 300_000.0
    assert network.get_node("N1").pressure_pa is not None


def test_hot_water_facade_from_network_computes_domain_network() -> None:
    network = _network("ECS")

    engine = HotWaterNetworkEngine.from_network(
        network=network,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    )

    result = engine.compute_all(
        source_node_id="N0",
        source_pressure_bar=3.0,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.section_count == 1
    assert result.value.section_results["S1"].sizing is not None
    assert result.value.section_results["S1"].sizing.demand.design_flow_l_s == 0.40
    assert network.get_node("N1").pressure_pa is not None


def test_compute_cold_water_network_from_domain_entry_point() -> None:
    network = _network("EFS")

    result = compute_cold_water_network_from_domain(
        network=network,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
        source_node_id="N0",
        source_pressure_bar=3.0,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.section_count == 1
    assert result.value.has_pressure_summary
    assert network.get_section("S1").selected_internal_diameter_mm is not None


def test_compute_hot_water_network_from_domain_entry_point() -> None:
    network = _network("ECS")

    result = compute_hot_water_network_from_domain(
        network=network,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
        source_node_id="N0",
        source_pressure_bar=3.0,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.section_count == 1
    assert result.value.has_pressure_summary
    assert network.get_section("S1").selected_internal_diameter_mm is not None


def test_public_network_api_exports_domain_entry_points() -> None:
    network = _network("EFS")

    result = compute_cold_water_network_from_network(
        network=network,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
        source_node_id="N0",
        source_pressure_bar=3.0,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.section_count == 1

    hot_network = _network("ECS")

    hot_result = compute_hot_water_network_from_network(
        network=hot_network,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
        source_node_id="N0",
        source_pressure_bar=3.0,
    )

    assert hot_result.ok
    assert hot_result.value is not None
    assert hot_result.value.section_count == 1


def test_facade_propagate_pressures_uses_existing_losses_without_resizing() -> None:
    network = _network("EFS")
    section = network.get_section("S1")
    section.total_pressure_loss_pa = 25_000.0

    engine = ColdWaterNetworkEngine.from_network(
        network=network,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    )

    result = engine.propagate_pressures(
        source_node_id="N0",
        source_pressure_pa=300_000.0,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.node_pressures["N1"].pressure_pa == 275_000.0
    assert section.selected_internal_diameter_mm is None