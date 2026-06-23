from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.catalogs.singular_loss_catalog import SingularLossCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.domain.fluids import Fluid
from ndc_core.domain.networks.section import Section
from ndc_core.hydraulics.total_pressure_loss import total_pressure_loss
from ndc_core.hydraulics.types import PressureLossBreakdown
from ndc_core.networks.domestic_water.types import DomesticWaterSide
from ndc_core.networks.domestic_water.section_state import apply_section_pressure_loss_state
from ndc_core.networks.domestic_water.singular_loss_rules import (
    collect_section_singular_zeta_values,
)
from ndc_core.networks.domestic_water.pipe_rules import (
    relative_roughness_for_section,
)
from ndc_core.networks.domestic_water.fluid_rules import (
    resolve_domestic_water_fluid,
)
from ndc_core.networks.domestic_water.section_hydraulic_inputs import (
    prepare_section_hydraulic_inputs,
)
from ndc_core.networks.domestic_water.pressure_loss_types import (
    DomesticWaterPressureLossMode,
)


@dataclass(frozen=True, slots=True)
class DomesticWaterPressureLossResult:
    """Pressure loss result for one domestic water section."""

    section_id: str
    side: DomesticWaterSide
    mode: DomesticWaterPressureLossMode
    fluid: Fluid
    breakdown: PressureLossBreakdown
    flow_l_s: float
    internal_diameter_mm: float | None
    length_m: float
    velocity_m_s: float
    relative_roughness_value: float
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @property
    def reynolds(self) -> float | None:
        return self.breakdown.reynolds

    @property
    def linear_pressure_loss_pa(self) -> float:
        return self.breakdown.linear_pressure_loss_pa

    @property
    def singular_pressure_loss_pa(self) -> float:
        return self.breakdown.singular_pressure_loss_pa

    @property
    def elevation_pressure_change_pa(self) -> float:
        return self.breakdown.elevation_pressure_change_pa

    @property
    def total_pressure_change_pa(self) -> float:
        return self.breakdown.total_pressure_change_pa

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)


@dataclass(frozen=True, slots=True)
class DomesticWaterPressureLossEngine:
    """
    Common EFS/ECS forward pressure loss engine.

    It consumes the sizing state written on Section by
    DomesticWaterSectionSizingEngine.
    """

    fluid_catalog: FluidCatalog
    pipe_catalog: PipeCatalog | None = None
    singular_loss_catalog: SingularLossCatalog | None = None
    side: DomesticWaterSide = DomesticWaterSide.COLD_WATER

    def compute_section_pressure_loss(
        self,
        section: Section,
        *,
        water_temperature_c: float | None = None,
        singular_zeta_values: Iterable[float | int | None] | None = None,
    ) -> Result[DomesticWaterPressureLossResult]:
        messages: list[EngineMessage] = []

        fluid = resolve_domestic_water_fluid(
            fluid_catalog=self.fluid_catalog,
            side=self.side,
            water_temperature_c=water_temperature_c,
            messages=messages,
        )
        if fluid is None:
            return Result.failure(messages=messages)

        inputs = prepare_section_hydraulic_inputs(
            section=section,
            messages=messages,
        )
        if inputs is None:
            return Result.failure(messages=messages)

        zeta_values = tuple(
            singular_zeta_values
            if singular_zeta_values is not None
            else collect_section_singular_zeta_values(
                section=section,
                singular_loss_catalog=self.singular_loss_catalog,
                flow_l_s=inputs.flow_l_s,
                velocity_m_s=inputs.velocity_m_s,
                density_kg_m3=fluid.density_kg_m3,
                messages=messages,
            )
        )

        roughness_value = relative_roughness_for_section(
            section=section,
            pipe_catalog=self.pipe_catalog,
            internal_diameter_m=inputs.internal_diameter_m,
        )

        breakdown = total_pressure_loss(
            velocity_m_s=inputs.velocity_m_s,
            internal_diameter_m=inputs.internal_diameter_m,
            length_m=inputs.length_m,
            density_kg_m3=fluid.density_kg_m3,
            kinematic_viscosity_m2_s=fluid.kinematic_viscosity_m2_s,
            relative_roughness_value=roughness_value,
            elevation_change_m=inputs.elevation_change_m,
            singular_zeta_values=zeta_values,
        )

        result = DomesticWaterPressureLossResult(
            section_id=section.id,
            side=self.side,
            mode=inputs.mode,
            fluid=fluid,
            breakdown=breakdown,
            flow_l_s=inputs.flow_l_s,
            internal_diameter_mm=inputs.internal_diameter_mm,
            length_m=inputs.length_m,
            velocity_m_s=inputs.velocity_m_s,
            relative_roughness_value=roughness_value,
            messages=tuple(messages),
        )

        apply_section_pressure_loss_state(section=section, pressure_loss=result)

        if result.has_errors:
            return Result.failure(value=result, messages=messages)

        return Result.success(value=result, messages=messages)


def compute_cold_water_section_pressure_loss(
    section: Section,
    fluid_catalog: FluidCatalog,
    *,
    pipe_catalog: PipeCatalog | None = None,
    singular_loss_catalog: SingularLossCatalog | None = None,
    water_temperature_c: float | None = None,
    singular_zeta_values: Iterable[float | int | None] | None = None,
) -> Result[DomesticWaterPressureLossResult]:
    """Convenience function for EFS section pressure loss."""

    return DomesticWaterPressureLossEngine(
        fluid_catalog=fluid_catalog,
        pipe_catalog=pipe_catalog,
        singular_loss_catalog=singular_loss_catalog,
        side=DomesticWaterSide.COLD_WATER,
    ).compute_section_pressure_loss(
        section=section,
        water_temperature_c=water_temperature_c,
        singular_zeta_values=singular_zeta_values,
    )


def compute_hot_water_section_pressure_loss(
    section: Section,
    fluid_catalog: FluidCatalog,
    *,
    pipe_catalog: PipeCatalog | None = None,
    singular_loss_catalog: SingularLossCatalog | None = None,
    water_temperature_c: float | None = None,
    singular_zeta_values: Iterable[float | int | None] | None = None,
) -> Result[DomesticWaterPressureLossResult]:
    """Convenience function for ECS forward section pressure loss."""

    return DomesticWaterPressureLossEngine(
        fluid_catalog=fluid_catalog,
        pipe_catalog=pipe_catalog,
        singular_loss_catalog=singular_loss_catalog,
        side=DomesticWaterSide.HOT_WATER,
    ).compute_section_pressure_loss(
        section=section,
        water_temperature_c=water_temperature_c,
        singular_zeta_values=singular_zeta_values,
    )