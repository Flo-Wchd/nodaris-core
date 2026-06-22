from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from ndc_core.domain.networks.types import DiameterMode, SectionUsageContext
from ndc_core.domain.singular_losses import SingularLoss


@dataclass(slots=True)
class Section:
    """
    Pipe section between two nodes.

    The section stores geometry, optional diameter forcing, singular losses and
    calculation state. It does not perform hydraulic computations by itself.
    """

    id: str
    name: str
    upstream_node_id: str
    downstream_node_id: str
    fluid_code: str
    usage_context: SectionUsageContext = SectionUsageContext.OTHER
    length_m: float = 0.0
    elevation_change_m: float = 0.0

    forced_pipe_size_code: str | None = None
    forced_internal_diameter_mm: float | None = None

    selected_pipe_size_code: str | None = None
    selected_internal_diameter_mm: float | None = None

    flow_l_s: float | None = None
    velocity_m_s: float | None = None

    linear_pressure_loss_pa: float | None = None
    singular_pressure_loss_pa: float | None = None
    elevation_pressure_loss_pa: float | None = None
    pressure_start_pa: float | None = None
    pressure_end_pa: float | None = None

    downstream_appliance_counts: dict[str, int] = field(default_factory=dict)
    effective_appliance_counts: dict[str, int] = field(default_factory=dict)
    singular_losses: list[SingularLoss] = field(default_factory=list)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.id = self.id.strip()
        self.name = self.name.strip()
        self.upstream_node_id = self.upstream_node_id.strip()
        self.downstream_node_id = self.downstream_node_id.strip()
        self.fluid_code = self.fluid_code.strip()

        self.length_m = max(0.0, self.length_m)

        if self.forced_internal_diameter_mm is not None:
            self.forced_internal_diameter_mm = max(0.0, self.forced_internal_diameter_mm)

        if self.selected_internal_diameter_mm is not None:
            self.selected_internal_diameter_mm = max(0.0, self.selected_internal_diameter_mm)

    @property
    def diameter_mode(self) -> DiameterMode:
        if self.forced_pipe_size_code:
            return DiameterMode.FORCED_PIPE

        if self.forced_internal_diameter_mm is not None:
            return DiameterMode.FORCED_INTERNAL_DIAMETER

        return DiameterMode.AUTOMATIC

    @property
    def has_forced_diameter(self) -> bool:
        return self.diameter_mode is not DiameterMode.AUTOMATIC

    @property
    def used_internal_diameter_mm(self) -> float | None:
        if self.forced_internal_diameter_mm is not None:
            return self.forced_internal_diameter_mm

        return self.selected_internal_diameter_mm

    @property
    def total_pressure_loss_pa(self) -> float | None:
        values = (
            self.linear_pressure_loss_pa,
            self.singular_pressure_loss_pa,
            self.elevation_pressure_loss_pa,
        )

        if all(value is None for value in values):
            return None

        return sum(value or 0.0 for value in values)

    def set_downstream_appliance_count(self, appliance_code: str, count: int) -> None:
        code = appliance_code.strip()
        if not code:
            return

        count = max(0, int(count))
        if count == 0:
            self.downstream_appliance_counts.pop(code, None)
            return

        self.downstream_appliance_counts[code] = count

    def set_effective_appliance_count(self, appliance_code: str, count: int) -> None:
        code = appliance_code.strip()
        if not code:
            return

        count = max(0, int(count))
        if count == 0:
            self.effective_appliance_counts.pop(code, None)
            return

        self.effective_appliance_counts[code] = count

    def add_singular_loss(self, singular_loss: SingularLoss) -> None:
        if singular_loss.is_active:
            self.singular_losses.append(singular_loss)

    def clear_calculation_state(self) -> None:
        """
        Clear calculation outputs while preserving geometry, topology and manual inputs.
        """

        self.selected_pipe_size_code = None
        self.selected_internal_diameter_mm = None

        self.flow_l_s = None
        self.velocity_m_s = None

        self.linear_pressure_loss_pa = None
        self.singular_pressure_loss_pa = None
        self.elevation_pressure_loss_pa = None
        self.pressure_start_pa = None
        self.pressure_end_pa = None

        self.downstream_appliance_counts.clear()
        self.effective_appliance_counts.clear()

    def as_debug_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "upstream_node_id": self.upstream_node_id,
            "downstream_node_id": self.downstream_node_id,
            "fluid_code": self.fluid_code,
            "usage_context": self.usage_context.value,
            "length_m": self.length_m,
            "elevation_change_m": self.elevation_change_m,
            "diameter_mode": self.diameter_mode.value,
            "forced_pipe_size_code": self.forced_pipe_size_code,
            "forced_internal_diameter_mm": self.forced_internal_diameter_mm,
            "selected_pipe_size_code": self.selected_pipe_size_code,
            "selected_internal_diameter_mm": self.selected_internal_diameter_mm,
            "used_internal_diameter_mm": self.used_internal_diameter_mm,
            "flow_l_s": self.flow_l_s,
            "velocity_m_s": self.velocity_m_s,
            "total_pressure_loss_pa": self.total_pressure_loss_pa,
            "downstream_appliance_counts": dict(self.downstream_appliance_counts),
            "effective_appliance_counts": dict(self.effective_appliance_counts),
            "singular_losses_count": len(self.singular_losses),
        }