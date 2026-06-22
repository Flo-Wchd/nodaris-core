from __future__ import annotations

from collections.abc import Iterable

from ndc_core.hydraulics.elevation_pressure_loss import elevation_pressure_change_pa
from ndc_core.hydraulics.friction import darcy_friction_factor
from ndc_core.hydraulics.linear_pressure_loss import linear_pressure_loss_pa
from ndc_core.hydraulics.reynolds import flow_regime, reynolds_number
from ndc_core.hydraulics.singular_pressure_loss import (
    singular_pressure_loss_pa,
    sum_zeta,
)
from ndc_core.hydraulics.types import PressureLossBreakdown


def total_pressure_loss(
    *,
    velocity_m_s: float,
    internal_diameter_m: float,
    length_m: float,
    density_kg_m3: float,
    kinematic_viscosity_m2_s: float,
    relative_roughness_value: float = 0.0,
    elevation_change_m: float = 0.0,
    singular_zeta_values: Iterable[float | int | None] | None = None,
) -> PressureLossBreakdown:
    """Return complete pressure loss breakdown for one section."""

    reynolds = reynolds_number(
        velocity_m_s=velocity_m_s,
        internal_diameter_m=internal_diameter_m,
        kinematic_viscosity_m2_s=kinematic_viscosity_m2_s,
    )

    regime = flow_regime(reynolds) if reynolds > 0.0 else None

    factor = (
        darcy_friction_factor(
            reynolds=reynolds,
            relative_roughness_value=relative_roughness_value,
        )
        if reynolds > 0.0
        else None
    )

    linear_loss = (
        linear_pressure_loss_pa(
            friction_factor=factor,
            length_m=length_m,
            internal_diameter_m=internal_diameter_m,
            velocity_m_s=velocity_m_s,
            density_kg_m3=density_kg_m3,
        )
        if factor is not None
        else 0.0
    )

    zeta_total = sum_zeta(singular_zeta_values)

    singular_loss = singular_pressure_loss_pa(
        zeta_total=zeta_total,
        velocity_m_s=velocity_m_s,
        density_kg_m3=density_kg_m3,
    )

    elevation_loss = elevation_pressure_change_pa(
        elevation_change_m=elevation_change_m,
        density_kg_m3=density_kg_m3,
    )

    return PressureLossBreakdown(
        reynolds=reynolds if reynolds > 0.0 else None,
        flow_regime=regime,
        friction_factor=factor,
        linear_pressure_loss_pa=linear_loss,
        singular_pressure_loss_pa=singular_loss,
        elevation_pressure_change_pa=elevation_loss,
        singular_zeta_total=zeta_total,
    )