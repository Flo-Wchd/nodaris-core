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
    DomesticWaterMessageBinder,
    DomesticWaterMessageBindingResult,
    bind_domestic_water_messages_to_entities,
    compute_cold_water_network_from_network,
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
        }
    )


def _pipe_catalog() -> PipeCatalog:
    material = PipeMaterial(
        code="EFS",
        name="EFS material",
        default_roughness_m=0.0000015,
    )
    size = PipeSize(
        code="EFS20",
        material_code="EFS",
        nominal_diameter="DN20",
        internal_diameter_mm=20.0,
    )

    return PipeCatalog(
        materials_by_code={"EFS": material},
        sizes_by_code={"EFS20": size},
        size_codes_by_material={"EFS": ["EFS20"]},
    )


def _fluid_catalog() -> FluidCatalog:
    cold = Fluid(
        code="cold_water",
        name="Cold water",
        temperature_c=10.0,
        density_kg_m3=1000.0,
        dynamic_viscosity_pa_s=0.001,
    )

    return FluidCatalog(
        fluids_by_code={
            "cold_water": cold,
        },
        water_points_by_temperature={
            10.0: cold,
        },
    )


def _network_with_cell() -> Network:
    network = Network(id="N", name="Network")

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
    cell = Cell(
        id="C1",
        name="Cell 1",
        appliance_counts={"L": 1},
    )
    section = Section(
        id="S1",
        name="S1",
        upstream_node_id="N0",
        downstream_node_id="N1",
        fluid_code="EFS",
        usage_context=SectionUsageContext.RISER,
        length_m=10.0,
    )

    network.add_node(source)
    network.add_node(terminal)
    network.add_cell(cell)
    network.add_section(section)
    network.attach_cell_to_node("C1", "N1")

    return network


def _network_without_appliances() -> Network:
    network = Network(id="N", name="Network")

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
        fluid_code="EFS",
        usage_context=SectionUsageContext.RISER,
        length_m=10.0,
    )

    network.add_node(source)
    network.add_node(terminal)
    network.add_section(section)

    return network


def test_compute_from_network_binds_messages_to_network_and_sections() -> None:
    network = _network_with_cell()

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

    section = network.get_section("S1")

    assert hasattr(network, "engine_messages")
    assert hasattr(network, "network_messages")
    assert hasattr(section, "engine_messages")
    assert hasattr(section, "section_messages")

    assert network.engine_messages == result.value.messages
    assert network.network_messages == result.value.messages

    assert isinstance(section.engine_messages, tuple)
    assert isinstance(section.section_messages, tuple)


def test_section_warning_is_bound_to_section_messages() -> None:
    network = _network_without_appliances()

    result = compute_cold_water_network_from_network(
        network=network,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    )

    assert result.value is not None

    section = network.get_section("S1")

    assert hasattr(section, "engine_messages")
    assert any(
        message.code == "DOMESTIC_WATER_NETWORK_SECTION_NO_APPLIANCES"
        for message in section.engine_messages
    )


def test_facade_from_network_keeps_message_binding() -> None:
    network = _network_with_cell()

    result = ColdWaterNetworkEngine.from_network(
        network=network,
        appliance_catalog=_appliance_catalog(),
        pipe_catalog=_pipe_catalog(),
        fluid_catalog=_fluid_catalog(),
    ).compute_all(
        source_node_id="N0",
        source_pressure_bar=3.0,
    )

    assert result.ok
    assert result.value is not None

    section = network.get_section("S1")

    assert hasattr(network, "engine_messages")
    assert hasattr(section, "engine_messages")
    assert network.engine_messages == result.value.messages


def test_public_api_exports_message_binding_tools() -> None:
    assert DomesticWaterMessageBinder is not None
    assert DomesticWaterMessageBindingResult is not None
    assert callable(bind_domestic_water_messages_to_entities)