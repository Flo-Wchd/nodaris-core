from __future__ import annotations

from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.domain.fluids import Fluid
from ndc_core.networks.domestic_water.types import DomesticWaterSide


def default_domestic_water_fluid_code(side: DomesticWaterSide) -> str:
    """Return the default fluid catalog code for a domestic water side."""

    if side is DomesticWaterSide.HOT_WATER:
        return "hot_water"

    return "cold_water"


def resolve_domestic_water_fluid(
    *,
    fluid_catalog: FluidCatalog,
    side: DomesticWaterSide,
    water_temperature_c: float | None,
    messages: list[EngineMessage],
) -> Fluid | None:
    """
    Resolve water properties for a domestic water pressure-loss calculation.

    Explicit temperature has priority over the side default. Missing catalog
    data is converted to managed engine messages instead of raising.
    """

    if water_temperature_c is not None:
        if not _temperature_is_inside_catalog_range(
                fluid_catalog=fluid_catalog,
                temperature_c=water_temperature_c,
        ):
            messages.append(
                EngineMessage.error(
                    code="DOMESTIC_WATER_FLUID_TEMPERATURE_UNKNOWN",
                    text="Water properties could not be resolved for requested temperature.",
                    context={"water_temperature_c": water_temperature_c},
                )
            )
            return None

        fluid = fluid_catalog.get_water_at_temperature(water_temperature_c)
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

    default_code = default_domestic_water_fluid_code(side)
    fluid = fluid_catalog.get(default_code)
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


def _temperature_is_inside_catalog_range(
    *,
    fluid_catalog: FluidCatalog,
    temperature_c: float,
) -> bool:
    temperatures = tuple(sorted(fluid_catalog.water_points_by_temperature))

    if not temperatures:
        return False

    return temperatures[0] <= temperature_c <= temperatures[-1]