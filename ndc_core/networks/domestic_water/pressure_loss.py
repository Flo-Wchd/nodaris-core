from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import StrEnum

from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.catalogs.singular_loss_catalog import SingularLossCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.domain.fluids import Fluid
from ndc_core.domain.networks.section import Section
from ndc_core.hydraulics.conversions import diameter_mm_to_m
from ndc_core.hydraulics.friction import relative_roughness
from ndc_core.hydraulics.total_pressure_loss import total_pressure_loss
from ndc_core.hydraulics.types import PressureLossBreakdown
from ndc_core.hydraulics.velocity import velocity_from_l_s_and_mm
from ndc_core.networks.domestic_water.types import DomesticWaterSide
from ndc_core.networks.domestic_water.entity_access import clean_optional_code
from ndc_core.networks.domestic_water.numeric import (
    safe_float,
    safe_positive_float,
)
from ndc_core.networks.domestic_water.section_state import apply_section_pressure_loss_state
from ndc_core.networks.domestic_water.singular_loss_rules import (
    collect_section_singular_zeta_values,
)


class DomesticWaterPressureLossMode(StrEnum):
    """Pressure loss calculation mode."""

    FULL = "full"
    ELEVATION_ONLY = "elevation_only"


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

        fluid = self._resolve_fluid(
            water_temperature_c=water_temperature_c,
            messages=messages,
        )
        if fluid is None:
            return Result.failure(messages=messages)

        flow_l_s = safe_positive_float(section.flow_l_s)
        diameter_mm = safe_positive_float(section.selected_internal_diameter_mm)

        if diameter_mm is None:
            messages.append(
                EngineMessage.error(
                    code="DOMESTIC_WATER_PRESSURE_DIAMETER_MISSING",
                    text="Section internal diameter is missing; pressure loss cannot be computed.",
                    context={"section_id": section.id},
                )
            )
            return Result.failure(messages=messages)

        length_m = max(0.0, safe_float(section.length_m))
        elevation_change_m = safe_float(section.elevation_change_m)

        if flow_l_s is None:
            mode = DomesticWaterPressureLossMode.ELEVATION_ONLY
            flow_for_calc_l_s = 0.0
            velocity_m_s = 0.0
            messages.append(
                EngineMessage.info(
                    code="DOMESTIC_WATER_PRESSURE_ELEVATION_ONLY",
                    text=(
                        "Section flow is zero or missing; only elevation pressure "
                        "change is computed."
                    ),
                    context={"section_id": section.id},
                )
            )
        else:
            mode = DomesticWaterPressureLossMode.FULL
            flow_for_calc_l_s = flow_l_s
            velocity_m_s = velocity_from_l_s_and_mm(
                flow_l_s=flow_l_s,
                internal_diameter_mm=diameter_mm,
            )

        diameter_m = diameter_mm_to_m(diameter_mm)

        zeta_values = tuple(
            singular_zeta_values
            if singular_zeta_values is not None
            else collect_section_singular_zeta_values(
                section=section,
                singular_loss_catalog=self.singular_loss_catalog,
                flow_l_s=flow_for_calc_l_s,
                velocity_m_s=velocity_m_s,
                density_kg_m3=fluid.density_kg_m3,
                messages=messages,
            )
        )

        roughness_value = self._relative_roughness_for_section(
            section=section,
            internal_diameter_m=diameter_m,
        )

        breakdown = total_pressure_loss(
            velocity_m_s=velocity_m_s,
            internal_diameter_m=diameter_m,
            length_m=length_m,
            density_kg_m3=fluid.density_kg_m3,
            kinematic_viscosity_m2_s=fluid.kinematic_viscosity_m2_s,
            relative_roughness_value=roughness_value,
            elevation_change_m=elevation_change_m,
            singular_zeta_values=zeta_values,
        )

        result = DomesticWaterPressureLossResult(
            section_id=section.id,
            side=self.side,
            mode=mode,
            fluid=fluid,
            breakdown=breakdown,
            flow_l_s=flow_for_calc_l_s,
            internal_diameter_mm=diameter_mm,
            length_m=length_m,
            velocity_m_s=velocity_m_s,
            relative_roughness_value=roughness_value,
            messages=tuple(messages),
        )

        apply_section_pressure_loss_state(section=section, pressure_loss=result)

        if result.has_errors:
            return Result.failure(value=result, messages=messages)

        return Result.success(value=result, messages=messages)

    def _resolve_fluid(
        self,
        *,
        water_temperature_c: float | None,
        messages: list[EngineMessage],
    ) -> Fluid | None:
        if water_temperature_c is not None:
            fluid = self.fluid_catalog.get_water_at_temperature(water_temperature_c)
            if fluid is not None:
                return fluid

            messages.append(
                EngineMessage.error(
                    code="DOMESTIC_WATER_FLUID_TEMPERATURE_UNKNOWN",
                    text="Water properties could not be resolved for requested temperature.",
                    context={"water_temperature_c": water_temperature_c},
                )
            )
            return None

        default_code = (
            "hot_water"
            if self.side is DomesticWaterSide.HOT_WATER
            else "cold_water"
        )
        fluid = self.fluid_catalog.get(default_code)
        if fluid is not None:
            return fluid

        messages.append(
            EngineMessage.error(
                code="DOMESTIC_WATER_FLUID_MISSING",
                text="Default water fluid is missing from the fluid catalog.",
                context={"fluid_code": default_code},
            )
        )
        return None

    def _relative_roughness_for_section(
        self,
        *,
        section: Section,
        internal_diameter_m: float,
    ) -> float:
        if self.pipe_catalog is None:
            return 0.0

        pipe_code = clean_optional_code(section.selected_pipe_size_code)
        if pipe_code is None:
            return 0.0

        pipe_size = self.pipe_catalog.get_size(pipe_code)
        if pipe_size is None:
            return 0.0

        material = self.pipe_catalog.materials_by_code.get(pipe_size.material_code)
        if material is None:
            return 0.0

        roughness_m = getattr(material, "default_roughness_m", 0.0)
        return relative_roughness(
            roughness_m=roughness_m,
            internal_diameter_m=internal_diameter_m,
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