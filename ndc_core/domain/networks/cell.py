from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(slots=True)
class Cell:
    """
    Local hydraulic cell.

    A cell represents a dwelling, room, sanitary block, technical room or any
    local group of appliances.

    It stores declared appliance quantities only. It does not apply DTU
    simultaneity rules and does not compute hydraulic flows.
    """

    id: str
    name: str
    cell_type: str | None = None
    building_id: str | None = None
    staircase_id: str | None = None
    level_label: str | None = None
    floor_index: int | None = None
    elevation_m: float | None = None
    notes: str | None = None
    appliance_counts: dict[str, int] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.id = self.id.strip()
        self.name = self.name.strip()
        self.appliance_counts = {
            self._normalize_appliance_code(code): max(0, int(count))
            for code, count in self.appliance_counts.items()
            if self._normalize_appliance_code(code) and int(count) > 0
        }

    @staticmethod
    def _normalize_appliance_code(value: object) -> str:
        return str(value or "").strip()

    def set_appliance_count(self, appliance_code: str, count: int) -> None:
        """Set an appliance quantity. A non-positive value removes the appliance."""

        code = self._normalize_appliance_code(appliance_code)
        if not code:
            return

        count = max(0, int(count))
        if count == 0:
            self.appliance_counts.pop(code, None)
            return

        self.appliance_counts[code] = count

    def add_appliance_count(self, appliance_code: str, count: int = 1) -> None:
        """Add a quantity to an appliance already declared in the cell."""

        code = self._normalize_appliance_code(appliance_code)
        if not code:
            return

        current = self.get_appliance_count(code)
        self.set_appliance_count(code, current + max(0, int(count)))

    def get_appliance_count(self, appliance_code: str) -> int:
        code = self._normalize_appliance_code(appliance_code)
        return max(0, int(self.appliance_counts.get(code, 0)))

    def remove_appliance(self, appliance_code: str) -> None:
        code = self._normalize_appliance_code(appliance_code)
        if code:
            self.appliance_counts.pop(code, None)

    @property
    def has_appliances(self) -> bool:
        return bool(self.appliance_counts)

    @property
    def total_appliance_count(self) -> int:
        return sum(max(0, int(count)) for count in self.appliance_counts.values())

    def copy_appliance_counts(self) -> dict[str, int]:
        return dict(self.appliance_counts)