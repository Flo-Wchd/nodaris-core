from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from ndc_core.domain.networks.cell import Cell
from ndc_core.domain.networks.types import NodeKind


@dataclass(slots=True)
class Node:
    """
    Topological network node.

    A node represents a source, junction, terminal point or equipment point.
    It can carry local cells but does not compute downstream demand.
    """

    id: str
    name: str
    kind: NodeKind = NodeKind.JUNCTION
    elevation_m: float | None = None
    pressure_pa: float | None = None
    local_zeta: float | None = None
    cells: list[Cell] = field(default_factory=list)
    upstream_section_ids: list[str] = field(default_factory=list)
    downstream_section_ids: list[str] = field(default_factory=list)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.id = self.id.strip()
        self.name = self.name.strip()

        if self.pressure_pa is not None:
            self.pressure_pa = max(0.0, self.pressure_pa)

        if self.local_zeta is not None:
            self.local_zeta = max(0.0, self.local_zeta)

    def attach_cell(self, cell: Cell) -> None:
        """Attach a cell if another cell with the same id is not already attached."""

        if not cell.id:
            return

        if all(existing.id != cell.id for existing in self.cells):
            self.cells.append(cell)

    def detach_cell(self, cell_id: str) -> None:
        normalized_id = cell_id.strip()
        self.cells = [cell for cell in self.cells if cell.id != normalized_id]

    def get_cell(self, cell_id: str) -> Cell | None:
        normalized_id = cell_id.strip()
        for cell in self.cells:
            if cell.id == normalized_id:
                return cell
        return None

    @property
    def has_cells(self) -> bool:
        return bool(self.cells)

    @property
    def local_appliance_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}

        for cell in self.cells:
            for code, count in cell.appliance_counts.items():
                counts[code] = counts.get(code, 0) + max(0, int(count))

        return counts

    def add_upstream_section_id(self, section_id: str) -> None:
        section_id = section_id.strip()
        if section_id and section_id not in self.upstream_section_ids:
            self.upstream_section_ids.append(section_id)

    def add_downstream_section_id(self, section_id: str) -> None:
        section_id = section_id.strip()
        if section_id and section_id not in self.downstream_section_ids:
            self.downstream_section_ids.append(section_id)

    def remove_section_id(self, section_id: str) -> None:
        section_id = section_id.strip()
        self.upstream_section_ids = [
            existing_id for existing_id in self.upstream_section_ids if existing_id != section_id
        ]
        self.downstream_section_ids = [
            existing_id for existing_id in self.downstream_section_ids if existing_id != section_id
        ]

    def set_pressure_bar(self, pressure_bar: float | None) -> None:
        if pressure_bar is None:
            self.pressure_pa = None
            return

        self.pressure_pa = max(0.0, pressure_bar * 100_000.0)

    def get_pressure_bar(self) -> float | None:
        if self.pressure_pa is None:
            return None

        return self.pressure_pa / 100_000.0

    def clear_pressure(self) -> None:
        self.pressure_pa = None