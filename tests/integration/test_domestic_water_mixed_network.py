from __future__ import annotations

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.domain.appliances import Appliance
from ndc_core.domain.fluids import Fluid
from ndc_core.domain.networks.cell import Cell
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


def _mixed_network() -> Network:
    """
    Mixed domestic water network.

    Topology:

        N0 source
        ├── S_EFS_1 → N_EFS terminal → Cell EFS
        └── S_ECS_1 → N_ECS terminal → Cell ECS

    The same domain Network contains both sides. Each facade must only compute
    the sections matching its side.
    """

    network = Network(id="N", name="Mixed EFS/ECS network")

    source = Node(
        id="N0",
        name="Source",
        kind=NodeKind.SOURCE,
    )
    cold_terminal = Node(
        id="N_EFS",
        name="Terminal EFS",
        kind=NodeKind.TERMINAL,
    )
    hot_terminal = Node(
        id="N_ECS",
        name="Terminal ECS",
        kind=NodeKind.TERMINAL,
    )

    cold_cell = Cell(
        id="C_EFS",
        name="Cell EFS",
        appliance_counts={
            "L": 1,
            "WC": 1,
        },
    )
    hot_cell = Cell(
        id="C_ECS",
        name="Cell ECS",
        appliance_counts={
            "L": 1,
            "D": 1,
        },
    )

    cold_section = Section(
        id="S_EFS_1",
        name="S_EFS_1",
        upstream_node_id="N0",
        downstream_node_id="N_EFS",
        fluid_code="EFS",
        usage_context=SectionUsageContext.RISER,
        length_m=10.0,
    )
    hot_section = Section(
        id="S_ECS_1",
        name="S_ECS_1",
        upstream_node_id="N0",
        downstream_node_id="N_ECS",
        fluid_code="ECS",
        usage_context=SectionUsageContext.RISER,
        length_m=8.0,
    )

    network.add_node(source)
    network.add_node(cold_terminal)
    network.add_node(hot_terminal)

    network.add_cell(cold_cell)
    network.add_cell(hot_cell)

    network.add_section(cold_section)
    network.add_section(hot_section)

    network.attach_cell_to_node("C_EFS", "N_EFS")
    network.attach_cell_to_node("C_ECS", "N_ECS")

    return network


def test_cold_water_engine_from_mixed_network_only_computes_cold_sections() -> None:
    network = _mixed_network()

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
    assert result.value.side is DomesticWaterSide.COLD_WATER
    assert set(result.value.section_results) == {"S_EFS_1"}

    cold_section = network.get_section("S_EFS_1")
    hot_section = network.get_section("S_ECS_1")

    assert cold_section.downstream_appliance_counts == {"L": 1, "WC": 1}
    assert cold_section.selected_internal_diameter_mm is not None
    assert cold_section.total_pressure_loss_pa is not None
    assert cold_section.pressure_start_pa == 300_000.0
    assert cold_section.pressure_end_pa is not None

    assert hot_section.downstream_appliance_counts == {}
    assert hot_section.selected_internal_diameter_mm is None
    assert hot_section.total_pressure_loss_pa is None
    assert hot_section.pressure_start_pa is None
    assert hot_section.pressure_end_pa is None


def test_hot_water_engine_from_mixed_network_only_computes_hot_sections() -> None:
    network = _mixed_network()

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
    assert result.value.side is DomesticWaterSide.HOT_WATER
    assert set(result.value.section_results) == {"S_ECS_1"}

    cold_section = network.get_section("S_EFS_1")
    hot_section = network.get_section("S_ECS_1")

    assert cold_section.downstream_appliance_counts == {}
    assert cold_section.selected_internal_diameter_mm is None
    assert cold_section.total_pressure_loss_pa is None
    assert cold_section.pressure_start_pa is None
    assert cold_section.pressure_end_pa is None

    assert hot_section.downstream_appliance_counts == {"L": 1, "D": 1}
    assert hot_section.effective_appliance_counts == {"L": 1, "D": 1}
    assert hot_section.selected_internal_diameter_mm is not None
    assert hot_section.total_pressure_loss_pa is not None
    assert hot_section.pressure_start_pa == 300_000.0
    assert hot_section.pressure_end_pa is not None

    sizing = result.value.section_results["S_ECS_1"].sizing

    assert sizing is not None
    assert sizing.demand.design_flow_l_s == 0.40


def test_functional_entry_points_from_mixed_network_keep_side_isolation() -> None:
    cold_network = _mixed_network()

    cold_result = compute_cold_water_network_from_network(
        network=cold_network,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
        source_node_id="N0",
        source_pressure_bar=3.0,
    )

    assert cold_result.ok
    assert cold_result.value is not None
    assert set(cold_result.value.section_results) == {"S_EFS_1"}

    assert cold_network.get_section("S_EFS_1").selected_internal_diameter_mm is not None
    assert cold_network.get_section("S_ECS_1").selected_internal_diameter_mm is None

    hot_network = _mixed_network()

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
    assert set(hot_result.value.section_results) == {"S_ECS_1"}

    assert hot_network.get_section("S_EFS_1").selected_internal_diameter_mm is None
    assert hot_network.get_section("S_ECS_1").selected_internal_diameter_mm is not None


def test_running_cold_then_hot_on_same_mixed_network_computes_both_without_cross_sizing() -> None:
    network = _mixed_network()

    cold_result = ColdWaterNetworkEngine.from_network(
        network=network,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    ).compute_all(
        source_node_id="N0",
        source_pressure_bar=3.0,
    )

    hot_result = HotWaterNetworkEngine.from_network(
        network=network,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    ).compute_all(
        source_node_id="N0",
        source_pressure_bar=3.0,
    )

    assert cold_result.ok
    assert hot_result.ok

    assert cold_result.value is not None
    assert hot_result.value is not None

    assert set(cold_result.value.section_results) == {"S_EFS_1"}
    assert set(hot_result.value.section_results) == {"S_ECS_1"}

    cold_section = network.get_section("S_EFS_1")
    hot_section = network.get_section("S_ECS_1")

    assert cold_section.selected_internal_diameter_mm is not None
    assert hot_section.selected_internal_diameter_mm is not None

    assert cold_section.fluid_code == "EFS"
    assert hot_section.fluid_code == "ECS"

    assert cold_section.downstream_appliance_counts == {"L": 1, "WC": 1}
    assert hot_section.downstream_appliance_counts == {"L": 1, "D": 1}

    assert cold_section.pressure_start_pa == 300_000.0
    assert hot_section.pressure_start_pa == 300_000.0
    assert cold_section.pressure_end_pa is not None
    assert hot_section.pressure_end_pa is not None