from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.catalogs.singular_loss_catalog import SingularLossCatalog
from ndc_core.common.result import Result
from ndc_core.common.messages import EngineMessage
from ndc_core.domain.networks.section import Section
from ndc_core.hydraulics.total_pressure_loss import total_pressure_loss
from ndc_core.networks.domestic_water.types import DomesticWaterSide
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
from ndc_core.networks.domestic_water.pressure_loss_result import (
    DomesticWaterPressureLossResult,
    build_section_pressure_loss_result,
)


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

        return build_section_pressure_loss_result(
            section=section,
            side=self.side,
            fluid=fluid,
            inputs=inputs,
            breakdown=breakdown,
            relative_roughness_value=roughness_value,
            messages=messages,
        )


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