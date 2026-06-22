from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.catalogs.singular_loss_catalog import SingularLossCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.domain.fluids import Fluid
from ndc_core.domain.networks.section import Section
from ndc_core.domain.singular_losses import SingularLoss, SingularLossMethod
from ndc_core.hydraulics.conversions import diameter_mm_to_m
from ndc_core.hydraulics.friction import relative_roughness
from ndc_core.hydraulics.singular_pressure_loss import equivalent_zeta_from_kv
from ndc_core.hydraulics.total_pressure_loss import total_pressure_loss
from ndc_core.hydraulics.types import PressureLossBreakdown
from ndc_core.hydraulics.velocity import velocity_from_l_s_and_mm
from ndc_core.networks.domestic_water.types import DomesticWaterSide


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

        flow_l_s = _safe_positive_float(section.flow_l_s)
        diameter_mm = _safe_positive_float(section.selected_internal_diameter_mm)

        if diameter_mm is None:
            messages.append(
                EngineMessage.error(
                    code="DOMESTIC_WATER_PRESSURE_DIAMETER_MISSING",
                    text="Section internal diameter is missing; pressure loss cannot be computed.",
                    context={"section_id": section.id},
                )
            )
            return Result.failure(messages=messages)

        length_m = max(0.0, _safe_float(section.length_m))
        elevation_change_m = _safe_float(section.elevation_change_m)

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
            else self._collect_section_zeta_values(
                section=section,
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

        _apply_pressure_loss_to_section(section=section, result=result)

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

        pipe_code = _clean_optional_code(section.selected_pipe_size_code)
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

    def _collect_section_zeta_values(
        self,
        *,
        section: Section,
        flow_l_s: float,
        velocity_m_s: float,
        density_kg_m3: float,
        messages: list[EngineMessage],
    ) -> tuple[float, ...]:
        zeta_values: list[float] = []

        for item in section.singular_losses:
            zeta = self._zeta_from_section_item(
                item=item,
                section=section,
                flow_l_s=flow_l_s,
                velocity_m_s=velocity_m_s,
                density_kg_m3=density_kg_m3,
                messages=messages,
            )
            if zeta > 0.0:
                zeta_values.append(zeta)

        return tuple(zeta_values)

    def _zeta_from_section_item(
        self,
        *,
        item: Any,
        section: Section,
        flow_l_s: float,
        velocity_m_s: float,
        density_kg_m3: float,
        messages: list[EngineMessage],
    ) -> float:
        quantity = _safe_positive_float(getattr(item, "quantity", 1.0)) or 1.0

        direct_zeta = _safe_positive_float(getattr(item, "zeta", None))
        if direct_zeta is not None:
            return direct_zeta * quantity

        loss_code = _clean_optional_code(
            getattr(item, "loss_code", None)
            or getattr(item, "singular_loss_code", None)
            or getattr(item, "code", None)
        )
        if loss_code is None:
            return 0.0

        if self.singular_loss_catalog is None:
            messages.append(
                EngineMessage.warning(
                    code="DOMESTIC_WATER_SINGULAR_CATALOG_MISSING",
                    text="Singular loss catalog is missing; section singular loss was ignored.",
                    context={
                        "section_id": section.id,
                        "loss_code": loss_code,
                    },
                )
            )
            return 0.0

        loss = self.singular_loss_catalog.get(loss_code)
        if loss is None:
            messages.append(
                EngineMessage.warning(
                    code="DOMESTIC_WATER_SINGULAR_LOSS_UNKNOWN",
                    text="Singular loss code is unknown; section singular loss was ignored.",
                    context={
                        "section_id": section.id,
                        "loss_code": loss_code,
                    },
                )
            )
            return 0.0

        return self._zeta_from_catalog_loss(
            loss=loss,
            quantity=quantity,
            section=section,
            flow_l_s=flow_l_s,
            velocity_m_s=velocity_m_s,
            density_kg_m3=density_kg_m3,
            messages=messages,
        )

    def _zeta_from_catalog_loss(
        self,
        *,
        loss: SingularLoss,
        quantity: float,
        section: Section,
        flow_l_s: float,
        velocity_m_s: float,
        density_kg_m3: float,
        messages: list[EngineMessage],
    ) -> float:
        if loss.method is SingularLossMethod.ZETA:
            return max(0.0, float(loss.zeta or 0.0)) * quantity

        if loss.method is SingularLossMethod.KV:
            if flow_l_s <= 0.0 or velocity_m_s <= 0.0:
                messages.append(
                    EngineMessage.warning(
                        code="DOMESTIC_WATER_KV_SKIPPED_NO_FLOW",
                        text="Kv singular loss was ignored because flow or velocity is missing.",
                        context={
                            "section_id": section.id,
                            "loss_code": loss.code,
                        },
                    )
                )
                return 0.0

            zeta = equivalent_zeta_from_kv(
                flow_l_s=flow_l_s,
                kv_m3_h=float(loss.kv or 0.0),
                velocity_m_s=velocity_m_s,
                density_kg_m3=density_kg_m3,
            )
            return zeta * quantity

        messages.append(
            EngineMessage.warning(
                code="DOMESTIC_WATER_SINGULAR_METHOD_UNSUPPORTED",
                text="Singular loss method is not supported yet for section pressure loss.",
                context={
                    "section_id": section.id,
                    "loss_code": loss.code,
                    "method": loss.method.value,
                },
            )
        )
        return 0.0


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


def _apply_pressure_loss_to_section(
    *,
    section: Section,
    result: DomesticWaterPressureLossResult,
) -> None:
    section.velocity_m_s = result.velocity_m_s
    section.reynolds = result.breakdown.reynolds
    section.friction_factor = result.breakdown.friction_factor
    section.linear_pressure_loss_pa = result.breakdown.linear_pressure_loss_pa
    section.singular_pressure_loss_pa = result.breakdown.singular_pressure_loss_pa
    section.elevation_pressure_loss_pa = (
        result.breakdown.elevation_pressure_change_pa
    )
    section.total_pressure_loss_pa = result.breakdown.total_pressure_change_pa
    section.singular_zeta_total = result.breakdown.singular_zeta_total


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _safe_positive_float(value: Any) -> float | None:
    if value is None:
        return None

    try:
        number = float(value)
    except (TypeError, ValueError):
        return None

    if number <= 0.0:
        return None

    return number


def _clean_optional_code(value: Any) -> str | None:
    text = str(value or "").strip()
    return text or None