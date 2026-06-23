from __future__ import annotations

from dataclasses import dataclass

from ndc_core.common.messages import EngineMessage
from ndc_core.domain.networks.section import Section
from ndc_core.hydraulics.conversions import diameter_mm_to_m
from ndc_core.hydraulics.velocity import velocity_from_l_s_and_mm
from ndc_core.networks.domestic_water.numeric import (
    safe_float,
    safe_positive_float,
)
from ndc_core.networks.domestic_water.pressure_loss_types import (
    DomesticWaterPressureLossMode,
)


@dataclass(frozen=True, slots=True)
class DomesticWaterSectionHydraulicInputs:
    """Hydraulic inputs prepared from a Section before pressure-loss calculation."""

    mode: DomesticWaterPressureLossMode
    flow_l_s: float
    internal_diameter_mm: float
    internal_diameter_m: float
    length_m: float
    elevation_change_m: float
    velocity_m_s: float


def prepare_section_hydraulic_inputs(
    *,
    section: Section,
    messages: list[EngineMessage],
) -> DomesticWaterSectionHydraulicInputs | None:
    """
    Prepare safe hydraulic inputs from a Section-like object.

    Returns None only when the section cannot be computed because its internal
    diameter is missing. Zero or missing flow is not an error: the calculation
    falls back to elevation-only mode.
    """

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
        return None

    length_m = max(0.0, safe_float(section.length_m))
    elevation_change_m = safe_float(section.elevation_change_m)

    if flow_l_s is None:
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
        return DomesticWaterSectionHydraulicInputs(
            mode=DomesticWaterPressureLossMode.ELEVATION_ONLY,
            flow_l_s=0.0,
            internal_diameter_mm=diameter_mm,
            internal_diameter_m=diameter_mm_to_m(diameter_mm),
            length_m=length_m,
            elevation_change_m=elevation_change_m,
            velocity_m_s=0.0,
        )

    return DomesticWaterSectionHydraulicInputs(
        mode=DomesticWaterPressureLossMode.FULL,
        flow_l_s=flow_l_s,
        internal_diameter_mm=diameter_mm,
        internal_diameter_m=diameter_mm_to_m(diameter_mm),
        length_m=length_m,
        elevation_change_m=elevation_change_m,
        velocity_m_s=velocity_from_l_s_and_mm(
            flow_l_s=flow_l_s,
            internal_diameter_mm=diameter_mm,
        ),
    )