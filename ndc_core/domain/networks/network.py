from __future__ import annotations

from dataclasses import dataclass, field

from ndc_core.common.messages import EngineMessage
from ndc_core.domain.networks.cell import Cell
from ndc_core.domain.networks.node import Node
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import NetworkKind, NodeKind


@dataclass(slots=True)
class Network:
    """
    Topological fluid network.

    The network owns nodes, sections and reusable cells. It provides safe editing
    and topology helpers. It does not perform hydraulic sizing.
    """

    id: str
    name: str
    kind: NetworkKind = NetworkKind.OTHER
    nodes: dict[str, Node] = field(default_factory=dict)
    sections: dict[str, Section] = field(default_factory=dict)
    cells: dict[str, Cell] = field(default_factory=dict)

    engine_messages: tuple[EngineMessage, ...] = field(default_factory=tuple)
    network_messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        self.id = self.id.strip()
        self.name = self.name.strip()

    def add_cell(self, cell: Cell) -> None:
        if cell.id:
            self.cells[cell.id] = cell

    def add_node(self, node: Node) -> None:
        if node.id:
            self.nodes[node.id] = node

    def add_section(self, section: Section) -> None:
        if not section.id:
            return

        self.sections[section.id] = section

        upstream_node = self.nodes.get(section.upstream_node_id)
        if upstream_node is not None:
            upstream_node.add_downstream_section_id(section.id)

        downstream_node = self.nodes.get(section.downstream_node_id)
        if downstream_node is not None:
            downstream_node.add_upstream_section_id(section.id)

    def get_cell(self, cell_id: str) -> Cell | None:
        return self.cells.get(cell_id.strip())

    def get_node(self, node_id: str) -> Node | None:
        return self.nodes.get(node_id.strip())

    def get_section(self, section_id: str) -> Section | None:
        return self.sections.get(section_id.strip())

    def attach_cell_to_node(self, cell_id: str, node_id: str) -> bool:
        cell = self.get_cell(cell_id)
        node = self.get_node(node_id)

        if cell is None or node is None:
            return False

        node.attach_cell(cell)
        return True

    def remove_section(self, section_id: str) -> None:
        section_id = section_id.strip()
        self.sections.pop(section_id, None)

        for node in self.nodes.values():
            node.remove_section_id(section_id)

    def remove_node(self, node_id: str) -> None:
        node_id = node_id.strip()
        if node_id not in self.nodes:
            return

        section_ids_to_remove = [
            section.id
            for section in self.sections.values()
            if section.upstream_node_id == node_id or section.downstream_node_id == node_id
        ]

        for section_id in section_ids_to_remove:
            self.remove_section(section_id)

        self.nodes.pop(node_id, None)

    def downstream_sections_of(self, node_id: str) -> list[Section]:
        node = self.get_node(node_id)
        if node is None:
            return []

        return [
            section
            for section_id in node.downstream_section_ids
            if (section := self.sections.get(section_id)) is not None
        ]

    def upstream_sections_of(self, node_id: str) -> list[Section]:
        node = self.get_node(node_id)
        if node is None:
            return []

        return [
            section
            for section_id in node.upstream_section_ids
            if (section := self.sections.get(section_id)) is not None
        ]

    @property
    def source_nodes(self) -> list[Node]:
        return [node for node in self.nodes.values() if node.kind is NodeKind.SOURCE]

    @property
    def terminal_nodes(self) -> list[Node]:
        terminals = [node for node in self.nodes.values() if node.kind is NodeKind.TERMINAL]
        if terminals:
            return terminals

        return [
            node
            for node in self.nodes.values()
            if not node.downstream_section_ids and node.kind is not NodeKind.SOURCE
        ]

    def clear_calculation_state(self) -> None:
        for section in self.sections.values():
            section.clear_calculation_state()

        for node in self.nodes.values():
            node.clear_pressure()

        self.engine_messages = ()
        self.network_messages = ()

    def validate_topology(self) -> tuple[EngineMessage, ...]:
        """
        Return managed topology messages.

        Validation is intentionally non-blocking. Callers decide whether errors
        prevent computation.
        """

        messages: list[EngineMessage] = []

        if not self.nodes:
            messages.append(
                EngineMessage.error(
                    code="NETWORK_NO_NODE",
                    text="The network does not contain any node.",
                    context={"network_id": self.id},
                )
            )

        if not self.sections:
            messages.append(
                EngineMessage.warning(
                    code="NETWORK_NO_SECTION",
                    text="The network does not contain any section.",
                    context={"network_id": self.id},
                )
            )

        for section in self.sections.values():
            if section.upstream_node_id not in self.nodes:
                messages.append(
                    EngineMessage.error(
                        code="SECTION_UNKNOWN_UPSTREAM_NODE",
                        text="A section references an unknown upstream node.",
                        context={
                            "network_id": self.id,
                            "section_id": section.id,
                            "upstream_node_id": section.upstream_node_id,
                        },
                    )
                )

            if section.downstream_node_id not in self.nodes:
                messages.append(
                    EngineMessage.error(
                        code="SECTION_UNKNOWN_DOWNSTREAM_NODE",
                        text="A section references an unknown downstream node.",
                        context={
                            "network_id": self.id,
                            "section_id": section.id,
                            "downstream_node_id": section.downstream_node_id,
                        },
                    )
                )

            if section.upstream_node_id == section.downstream_node_id:
                messages.append(
                    EngineMessage.error(
                        code="SECTION_SAME_ENDPOINTS",
                        text="A section cannot have identical upstream and downstream nodes.",
                        context={
                            "network_id": self.id,
                            "section_id": section.id,
                            "node_id": section.upstream_node_id,
                        },
                    )
                )

        return tuple(messages)