from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ndc_core.networks.domestic_water.appliance_counts import (
    normalize_appliance_counts,
)


def apply_section_sizing_state(
    *,
    section: Any,
    sizing: Any,
    raw_counts: Mapping[str, int],
    effective_counts: Mapping[str, int],
) -> None:
    """
    Apply domestic water sizing outputs to a Section-like object.

    This is the single write point for:
    - flow;
    - velocity;
    - declared downstream appliance counts;
    - effective appliance counts;
    - selected pipe size;
    - selected internal diameter.
    """

    section.flow_l_s = sizing.demand.design_flow_l_s
    section.velocity_m_s = sizing.velocity_m_s

    _replace_mapping_attribute(
        entity=section,
        attribute_name="downstream_appliance_counts",
        values=normalize_appliance_counts(raw_counts),
    )
    _replace_mapping_attribute(
        entity=section,
        attribute_name="effective_appliance_counts",
        values=normalize_appliance_counts(effective_counts),
    )

    section.selected_pipe_size_code = sizing.selected_pipe_size_code
    section.selected_internal_diameter_mm = sizing.used_internal_diameter_mm


def apply_section_pressure_loss_state(
    *,
    section: Any,
    pressure_loss: Any,
) -> None:
    """
    Apply domestic water pressure-loss outputs to a Section-like object.

    This is the single write point for:
    - velocity;
    - Reynolds number;
    - friction factor;
    - linear pressure loss;
    - singular pressure loss;
    - elevation pressure change;
    - total pressure loss;
    - total singular zeta.
    """

    breakdown = pressure_loss.breakdown

    section.velocity_m_s = pressure_loss.velocity_m_s
    section.reynolds = breakdown.reynolds
    section.friction_factor = breakdown.friction_factor
    section.linear_pressure_loss_pa = breakdown.linear_pressure_loss_pa
    section.singular_pressure_loss_pa = breakdown.singular_pressure_loss_pa
    section.elevation_pressure_loss_pa = breakdown.elevation_pressure_change_pa
    section.total_pressure_loss_pa = breakdown.total_pressure_change_pa
    section.singular_zeta_total = breakdown.singular_zeta_total


def _replace_mapping_attribute(
    *,
    entity: Any,
    attribute_name: str,
    values: Mapping[str, int],
) -> None:
    target = getattr(entity, attribute_name, None)

    if isinstance(target, dict):
        target.clear()
        target.update(values)
        return

    try:
        setattr(entity, attribute_name, dict(values))
    except (AttributeError, TypeError):
        return