from ndc_core.domain.networks.cell import Cell
from ndc_core.domain.networks.node import Node
from ndc_core.domain.networks.types import NodeKind


def test_node_normalizes_identity() -> None:
    node = Node(id=" N1 ", name=" Source ", kind=NodeKind.SOURCE)

    assert node.id == "N1"
    assert node.name == "Source"
    assert node.kind is NodeKind.SOURCE


def test_node_attach_cell_once() -> None:
    node = Node(id="N1", name="Node")
    cell = Cell(id="C1", name="Cell")

    node.attach_cell(cell)
    node.attach_cell(cell)

    assert node.has_cells
    assert len(node.cells) == 1
    assert node.get_cell("C1") is cell


def test_node_detach_cell() -> None:
    node = Node(id="N1", name="Node")
    node.attach_cell(Cell(id="C1", name="Cell"))

    node.detach_cell("C1")

    assert not node.has_cells


def test_node_local_appliance_counts() -> None:
    node = Node(id="N1", name="Node")
    node.attach_cell(Cell(id="C1", name="Cell 1", appliance_counts={"lavabo": 1}))
    node.attach_cell(Cell(id="C2", name="Cell 2", appliance_counts={"lavabo": 2, "wc": 1}))

    assert node.local_appliance_counts == {"lavabo": 3, "wc": 1}


def test_node_section_references() -> None:
    node = Node(id="N1", name="Node")

    node.add_upstream_section_id("S0")
    node.add_downstream_section_id("S1")
    node.add_downstream_section_id("S1")

    assert node.upstream_section_ids == ["S0"]
    assert node.downstream_section_ids == ["S1"]

    node.remove_section_id("S1")

    assert node.upstream_section_ids == ["S0"]
    assert node.downstream_section_ids == []


def test_node_pressure_helpers() -> None:
    node = Node(id="N1", name="Node")

    node.set_pressure_bar(3.0)

    assert node.pressure_pa == 300_000.0
    assert node.get_pressure_bar() == 3.0

    node.clear_pressure()

    assert node.pressure_pa is None