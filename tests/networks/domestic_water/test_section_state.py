from __future__ import annotations

from dataclasses import dataclass, field
from types import SimpleNamespace

from ndc_core.networks.domestic_water.section_state import (
    apply_section_pressure_loss_state,
    apply_section_sizing_state,
)


@dataclass
class _Section:
    flow_l_s: float | None = None
    velocity_m_s: float | None = None
    downstream_appliance_counts: dict[str, int] = field(default_factory=dict)
    effective_appliance_counts: dict[str, int] = field(default_factory=dict)
    selected_pipe_size_code: str | None = None
    selected_internal_diameter_mm: float | None = None
    reynolds: float | None = None
    friction_factor: float | None = None
    linear_pressure_loss_pa: float | None = None
    singular_pressure_loss_pa: float | None = None
    elevation_pressure_loss_pa: float | None = None
    total_pressure_loss_pa: float | None = None
    singular_zeta_total: float | None = None


def test_apply_section_sizing_state() -> None:
    section = _Section(
        downstream_appliance_counts={"OLD": 1},
        effective_appliance_counts={"OLD": 1},
    )
    sizing = SimpleNamespace(
        demand=SimpleNamespace(design_flow_l_s=0.52),
        velocity_m_s=1.12,
        selected_pipe_size_code="P20",
        used_internal_diameter_mm=20.0,
    )

    apply_section_sizing_state(
        section=section,
        sizing=sizing,
        raw_counts={
            "L": 1,
            "D": "2",
            "BAD": 0,
        },
        effective_counts={
            "L": 1,
            "D": 1,
        },
    )

    assert section.flow_l_s == 0.52
    assert section.velocity_m_s == 1.12
    assert section.downstream_appliance_counts == {"L": 1, "D": 2}
    assert section.effective_appliance_counts == {"L": 1, "D": 1}
    assert section.selected_pipe_size_code == "P20"
    assert section.selected_internal_diameter_mm == 20.0


def test_apply_section_pressure_loss_state() -> None:
    section = _Section()
    pressure_loss = SimpleNamespace(
        velocity_m_s=0.64,
        breakdown=SimpleNamespace(
            reynolds=12_345.0,
            friction_factor=0.021,
            linear_pressure_loss_pa=1_000.0,
            singular_pressure_loss_pa=250.0,
            elevation_pressure_change_pa=9_810.0,
            total_pressure_change_pa=11_060.0,
            singular_zeta_total=2.0,
        ),
    )

    apply_section_pressure_loss_state(
        section=section,
        pressure_loss=pressure_loss,
    )

    assert section.velocity_m_s == 0.64
    assert section.reynolds == 12_345.0
    assert section.friction_factor == 0.021
    assert section.linear_pressure_loss_pa == 1_000.0
    assert section.singular_pressure_loss_pa == 250.0
    assert section.elevation_pressure_loss_pa == 9_810.0
    assert section.total_pressure_loss_pa == 11_060.0
    assert section.singular_zeta_total == 2.0