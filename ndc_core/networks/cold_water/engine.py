from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.catalogs.singular_loss_catalog import SingularLossCatalog
from ndc_core.common.result import Result
from ndc_core.networks.domestic_water.network_engine import (
    DomesticWaterNetworkComputeResult,
    DomesticWaterNetworkEngine,
)
from ndc_core.networks.domestic_water.pressure_network import (
    DomesticWaterPressurePropagationResult,
    DomesticWaterPressureSummary,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


@dataclass(frozen=True, slots=True)
class ColdWaterNetworkEngine:
    """
    Professional EFS facade.

    This class is intentionally thin. It exposes a cold-water-oriented API while
    delegating all hydraulic work to the common domestic water engine.
    """

    nodes: Mapping[str, Any]
    sections: Mapping[str, Any]
    appliance_catalog: ApplianceCatalog
    pipe_catalog: PipeCatalog
    fluid_catalog: FluidCatalog
    singular_loss_catalog: SingularLossCatalog | None = None

    @property
    def side(self) -> DomesticWaterSide:
        return DomesticWaterSide.COLD_WATER

    def domestic_engine(self) -> DomesticWaterNetworkEngine:
        return DomesticWaterNetworkEngine.cold_water(
            nodes=self.nodes,
            sections=self.sections,
            appliance_catalog=self.appliance_catalog,
            pipe_catalog=self.pipe_catalog,
            fluid_catalog=self.fluid_catalog,
            singular_loss_catalog=self.singular_loss_catalog,
        )

    def compute_sections(
        self,
        *,
        max_velocity_m_s: float | None = None,
        water_temperature_c: float | None = None,
    ) -> Result[DomesticWaterNetworkComputeResult]:
        """
        Compute EFS section sizing and pressure losses.

        Pressure propagation is not run by this method.
        """

        return self.domestic_engine().compute_sections(
            max_velocity_m_s=max_velocity_m_s,
            water_temperature_c=water_temperature_c,
        )

    def compute_all(
        self,
        *,
        source_node_id: str | None = None,
        source_pressure_bar: float | None = None,
        min_required_pressure_bar: float = 1.0,
        max_velocity_m_s: float | None = None,
        water_temperature_c: float | None = None,
    ) -> Result[DomesticWaterNetworkComputeResult]:
        """
        Compute full EFS network.

        Pipeline:
        - section sizing;
        - section pressure losses;
        - optional pressure propagation;
        - optional worst terminal pressure summary.
        """

        return self.domestic_engine().compute_all(
            source_node_id=source_node_id,
            source_pressure_bar=source_pressure_bar,
            min_required_pressure_bar=min_required_pressure_bar,
            max_velocity_m_s=max_velocity_m_s,
            water_temperature_c=water_temperature_c,
        )

    def propagate_pressures(
        self,
        *,
        source_node_id: str,
        source_pressure_pa: float,
    ) -> Result[DomesticWaterPressurePropagationResult]:
        """
        Propagate EFS pressures using already computed section pressure losses.
        """

        return self.domestic_engine().compute_all(
            source_node_id=source_node_id,
            source_pressure_bar=source_pressure_pa / 100_000.0,
        ).with_value(
            lambda value: value.pressure_propagation if value else None
        )

    def summarize_worst_terminal_pressure(
        self,
        *,
        source_node_id: str,
        source_pressure_bar: float,
        min_required_pressure_bar: float = 1.0,
    ) -> Result[DomesticWaterPressureSummary]:
        """
        Compute EFS worst terminal pressure summary.
        """

        return self.domestic_engine().compute_all(
            source_node_id=source_node_id,
            source_pressure_bar=source_pressure_bar,
            min_required_pressure_bar=min_required_pressure_bar,
        ).with_value(
            lambda value: value.pressure_summary if value else None
        )


def compute_cold_water_network(
    *,
    nodes: Mapping[str, Any],
    sections: Mapping[str, Any],
    appliance_catalog: ApplianceCatalog,
    pipe_catalog: PipeCatalog,
    fluid_catalog: FluidCatalog,
    singular_loss_catalog: SingularLossCatalog | None = None,
    source_node_id: str | None = None,
    source_pressure_bar: float | None = None,
    min_required_pressure_bar: float = 1.0,
    max_velocity_m_s: float | None = None,
    water_temperature_c: float | None = None,
) -> Result[DomesticWaterNetworkComputeResult]:
    """
    Functional EFS entry point.
    """

    return ColdWaterNetworkEngine(
        nodes=nodes,
        sections=sections,
        appliance_catalog=appliance_catalog,
        pipe_catalog=pipe_catalog,
        fluid_catalog=fluid_catalog,
        singular_loss_catalog=singular_loss_catalog,
    ).compute_all(
        source_node_id=source_node_id,
        source_pressure_bar=source_pressure_bar,
        min_required_pressure_bar=min_required_pressure_bar,
        max_velocity_m_s=max_velocity_m_s,
        water_temperature_c=water_temperature_c,
    )