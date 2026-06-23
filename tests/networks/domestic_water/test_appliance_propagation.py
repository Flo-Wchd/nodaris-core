from __future__ import annotations

from ndc_core.domain.networks.cell import Cell
from ndc_core.domain.networks.network import Network
from ndc_core.domain.networks.node import Node
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import NodeKind, SectionUsageContext
from ndc_core.networks.domestic_water.appliance_propagation import (
    propagate_cold_water_appliances,
    propagate_hot_water_appliances,
)


def _node(node_id: str, kind: NodeKind = NodeKind.JUNCTION) -> Node:
    return Node(
        id=node_id,
        name=node_id,
        kind=kind,
    )


def _section(
    section_id: str,
    upstream_node_id: str,
    downstream_node_id: str,
    *,
    fluid_code: str = "EFS",
) -> Section:
    return Section(
        id=section_id,
        name=section_id,
        upstream_node_id=upstream_node_id,
        downstream_node_id=downstream_node_id,
        fluid_code=fluid_code,
        usage_context=SectionUsageContext.RISER,
        length_m=1.0,
    )


def test_propagates_terminal_cell_appliances_to_upstream_sections() -> None:
    network = Network(id="N", name="Network")

    source = _node("N0", NodeKind.SOURCE)
    junction = _node("N1")
    terminal = _node("N2", NodeKind.TERMINAL)

    cell = Cell(
        id="C1",
        name="Cell 1",
        appliance_counts={"L": 1, "D": 1},
    )

    network.add_node(source)
    network.add_node(junction)
    network.add_node(terminal)
    network.add_cell(cell)

    network.add_section(_section("S1", "N0", "N1"))
    network.add_section(_section("S2", "N1", "N2"))
    network.attach_cell_to_node("C1", "N2")

    result = propagate_cold_water_appliances(
        nodes=network.nodes,
        sections=network.sections,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.propagated

    assert network.get_section("S1").downstream_appliance_counts == {"L": 1, "D": 1}
    assert network.get_section("S2").downstream_appliance_counts == {"L": 1, "D": 1}


def test_propagates_branch_appliances_independently() -> None:
    network = Network(id="N", name="Network")

    source = _node("N0", NodeKind.SOURCE)
    left = _node("N1", NodeKind.TERMINAL)
    right = _node("N2", NodeKind.TERMINAL)

    left_cell = Cell(
        id="C1",
        name="Left cell",
        appliance_counts={"L": 1},
    )
    right_cell = Cell(
        id="C2",
        name="Right cell",
        appliance_counts={"D": 1},
    )

    network.add_node(source)
    network.add_node(left)
    network.add_node(right)
    network.add_cell(left_cell)
    network.add_cell(right_cell)

    network.add_section(_section("S1", "N0", "N1"))
    network.add_section(_section("S2", "N0", "N2"))

    network.attach_cell_to_node("C1", "N1")
    network.attach_cell_to_node("C2", "N2")

    result = propagate_cold_water_appliances(
        nodes=network.nodes,
        sections=network.sections,
    )

    assert result.ok
    assert result.value is not None

    assert network.get_section("S1").downstream_appliance_counts == {"L": 1}
    assert network.get_section("S2").downstream_appliance_counts == {"D": 1}
    assert result.value.node_downstream_counts["N0"] == {"L": 1, "D": 1}


def test_no_local_appliances_preserves_manual_section_counts() -> None:
    network = Network(id="N", name="Network")

    network.add_node(_node("N0", NodeKind.SOURCE))
    network.add_node(_node("N1", NodeKind.TERMINAL))

    section = _section("S1", "N0", "N1")
    section.downstream_appliance_counts.update({"L": 2})

    network.add_section(section)

    result = propagate_cold_water_appliances(
        nodes=network.nodes,
        sections=network.sections,
    )

    assert result.ok
    assert result.value is not None
    assert not result.value.propagated
    assert section.downstream_appliance_counts == {"L": 2}


def test_hot_water_propagation_ignores_cold_water_sections() -> None:
    network = Network(id="N", name="Network")

    source = _node("N0", NodeKind.SOURCE)
    terminal = _node("N1", NodeKind.TERMINAL)
    cell = Cell(
        id="C1",
        name="Cell 1",
        appliance_counts={"L": 1},
    )

    network.add_node(source)
    network.add_node(terminal)
    network.add_cell(cell)

    section = _section("S1", "N0", "N1", fluid_code="EFS")
    network.add_section(section)
    network.attach_cell_to_node("C1", "N1")

    result = propagate_hot_water_appliances(
        nodes=network.nodes,
        sections=network.sections,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.propagated
    assert section.downstream_appliance_counts == {}


def test_cycle_is_reported_without_exception() -> None:
    network = Network(id="N", name="Network")

    n0 = _node("N0")
    n1 = _node("N1")
    cell = Cell(
        id="C1",
        name="Cell 1",
        appliance_counts={"L": 1},
    )

    network.add_node(n0)
    network.add_node(n1)
    network.add_cell(cell)

    network.add_section(_section("S1", "N0", "N1"))
    network.add_section(_section("S2", "N1", "N0"))
    network.attach_cell_to_node("C1", "N1")

    result = propagate_cold_water_appliances(
        nodes=network.nodes,
        sections=network.sections,
    )

    assert result.failed
    assert result.value is not None
    assert result.value.has_errors
    assert any(
        message.code == "DOMESTIC_WATER_APPLIANCE_GRAPH_CYCLE"
        for message in result.messages
    )