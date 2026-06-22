from ndc_core.domain.networks.cell import Cell
from ndc_core.domain.networks.network import Network
from ndc_core.domain.networks.node import Node
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import NetworkKind, NodeKind


def test_network_add_entities() -> None:
    network = Network(id="NW1", name="Network", kind=NetworkKind.COLD_WATER)
    cell = Cell(id="C1", name="Cell")
    source = Node(id="N1", name="Source", kind=NodeKind.SOURCE)
    terminal = Node(id="N2", name="Terminal", kind=NodeKind.TERMINAL)
    section = Section(
        id="S1",
        name="Section",
        upstream_node_id="N1",
        downstream_node_id="N2",
        fluid_code="EFS",
    )

    network.add_cell(cell)
    network.add_node(source)
    network.add_node(terminal)
    network.add_section(section)

    assert network.get_cell("C1") is cell
    assert network.get_node("N1") is source
    assert network.get_section("S1") is section
    assert source.downstream_section_ids == ["S1"]
    assert terminal.upstream_section_ids == ["S1"]


def test_network_attach_cell_to_node() -> None:
    network = Network(id="NW1", name="Network")
    network.add_cell(Cell(id="C1", name="Cell"))
    network.add_node(Node(id="N1", name="Node"))

    attached = network.attach_cell_to_node("C1", "N1")

    assert attached
    assert network.get_node("N1") is not None
    assert network.get_node("N1").has_cells  # type: ignore[union-attr]


def test_network_attach_cell_to_unknown_node_returns_false() -> None:
    network = Network(id="NW1", name="Network")
    network.add_cell(Cell(id="C1", name="Cell"))

    assert not network.attach_cell_to_node("C1", "UNKNOWN")


def test_network_downstream_and_upstream_sections() -> None:
    network = Network(id="NW1", name="Network")
    network.add_node(Node(id="N1", name="Node 1"))
    network.add_node(Node(id="N2", name="Node 2"))
    section = Section(
        id="S1",
        name="Section",
        upstream_node_id="N1",
        downstream_node_id="N2",
        fluid_code="EFS",
    )
    network.add_section(section)

    assert network.downstream_sections_of("N1") == [section]
    assert network.upstream_sections_of("N2") == [section]


def test_network_source_and_terminal_nodes() -> None:
    network = Network(id="NW1", name="Network")
    source = Node(id="N1", name="Source", kind=NodeKind.SOURCE)
    terminal = Node(id="N2", name="Terminal", kind=NodeKind.TERMINAL)

    network.add_node(source)
    network.add_node(terminal)

    assert network.source_nodes == [source]
    assert network.terminal_nodes == [terminal]


def test_network_remove_section_updates_nodes() -> None:
    network = Network(id="NW1", name="Network")
    network.add_node(Node(id="N1", name="Node 1"))
    network.add_node(Node(id="N2", name="Node 2"))
    network.add_section(
        Section(
            id="S1",
            name="Section",
            upstream_node_id="N1",
            downstream_node_id="N2",
            fluid_code="EFS",
        )
    )

    network.remove_section("S1")

    assert network.sections == {}
    assert network.get_node("N1").downstream_section_ids == []  # type: ignore[union-attr]
    assert network.get_node("N2").upstream_section_ids == []  # type: ignore[union-attr]


def test_network_validate_topology_detects_missing_node() -> None:
    network = Network(id="NW1", name="Network")
    network.add_node(Node(id="N1", name="Node 1"))
    network.add_section(
        Section(
            id="S1",
            name="Section",
            upstream_node_id="N1",
            downstream_node_id="UNKNOWN",
            fluid_code="EFS",
        )
    )

    messages = network.validate_topology()

    assert any(message.code == "SECTION_UNKNOWN_DOWNSTREAM_NODE" for message in messages)
    assert any(message.is_error for message in messages)


def test_network_clear_calculation_state() -> None:
    network = Network(id="NW1", name="Network")
    node = Node(id="N1", name="Node")
    node.set_pressure_bar(3.0)
    section = Section(
        id="S1",
        name="Section",
        upstream_node_id="N1",
        downstream_node_id="N1",
        fluid_code="EFS",
    )
    section.flow_l_s = 0.2

    network.add_node(node)
    network.add_section(section)

    network.clear_calculation_state()

    assert node.pressure_pa is None
    assert section.flow_l_s is None