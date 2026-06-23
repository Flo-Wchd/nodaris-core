from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.catalogs.singular_loss_catalog import SingularLossCatalog
from ndc_core.common.result import Result
from ndc_core.domain.networks.network import Network
from ndc_core.networks.domestic_water.network_engine import (
    DomesticWaterNetworkComputeResult,
    DomesticWaterNetworkEngine,
    compute_hot_water_network_from_domain,
)
from ndc_core.networks.domestic_water.pressure_network import (
    DomesticWaterPressureNetworkEngine,
    DomesticWaterPressurePropagationResult,
    DomesticWaterPressureSummary,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


@dataclass(frozen=True, slots=True)
class HotWaterNetworkEngine:
    """
    Professional ECS facade.

    This class is intentionally thin. It exposes a hot-water-oriented API while
    delegating all forward ECS hydraulic work to the common domestic water engine.
    """

    nodes: Mapping[str, Any]
    sections: Mapping[str, Any]
    appliance_catalog: ApplianceCatalog
    pipe_catalog: PipeCatalog
    fluid_catalog: FluidCatalog
    singular_loss_catalog: SingularLossCatalog | None = None
    network: Network | None = None

    @classmethod
    def from_network(
        cls,
        *,
        network: Network,
        appliance_catalog: ApplianceCatalog,
        pipe_catalog: PipeCatalog,
        fluid_catalog: FluidCatalog,
        singular_loss_catalog: SingularLossCatalog | None = None,
    ) -> HotWaterNetworkEngine:
        """
        Build an ECS facade from the domain Network object.
        """

        return cls(
            nodes=network.nodes,
            sections=network.sections,
            appliance_catalog=appliance_catalog,
            pipe_catalog=pipe_catalog,
            fluid_catalog=fluid_catalog,
            singular_loss_catalog=singular_loss_catalog,
            network=network,
        )

    @property
    def side(self) -> DomesticWaterSide:
        return DomesticWaterSide.HOT_WATER

    def domestic_engine(self) -> DomesticWaterNetworkEngine:
        if self.network is not None:
            return DomesticWaterNetworkEngine.hot_water_from_network(
                network=self.network,
                appliance_catalog=self.appliance_catalog,
                pipe_catalog=self.pipe_catalog,
                fluid_catalog=self.fluid_catalog,
                singular_loss_catalog=self.singular_loss_catalog,
            )

        return DomesticWaterNetworkEngine.hot_water(
            nodes=self.nodes,
            sections=self.sections,
            appliance_catalog=self.appliance_catalog,
            pipe_catalog=self.pipe_catalog,
            fluid_catalog=self.fluid_catalog,
            singular_loss_catalog=self.singular_loss_catalog,
        )

    def pressure_network_engine(self) -> DomesticWaterPressureNetworkEngine:
        return DomesticWaterPressureNetworkEngine(
            nodes=self.nodes,
            sections=self.sections,
            side=self.side,
        )

    def compute_sections(
        self,
        *,
        max_velocity_m_s: float | None = None,
        water_temperature_c: float | None = None,
    ) -> Result[DomesticWaterNetworkComputeResult]:
        """
        Compute ECS section sizing and pressure losses.

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
        Compute full ECS forward network.

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
        Propagate ECS pressures using already computed section pressure losses.
        """

        return self.pressure_network_engine().propagate_pressures(
            source_node_id=source_node_id,
            source_pressure_pa=source_pressure_pa,
        )

    def summarize_worst_terminal_pressure(
        self,
        *,
        source_node_id: str,
        source_pressure_bar: float,
        min_required_pressure_bar: float = 1.0,
    ) -> Result[DomesticWaterPressureSummary]:
        """
        Compute ECS worst terminal pressure summary from existing pressure losses.
        """

        return self.pressure_network_engine().summarize_worst_terminal_pressure(
            source_node_id=source_node_id,
            source_pressure_bar=source_pressure_bar,
            min_required_pressure_bar=min_required_pressure_bar,
        )


def compute_hot_water_network(
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
    Functional ECS forward entry point.
    """

    return HotWaterNetworkEngine(
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


def compute_hot_water_network_from_network(
    *,
    network: Network,
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
    Functional ECS forward entry point from the domain Network aggregate.
    """

    return compute_hot_water_network_from_domain(
        network=network,
        appliance_catalog=appliance_catalog,
        pipe_catalog=pipe_catalog,
        fluid_catalog=fluid_catalog,
        singular_loss_catalog=singular_loss_catalog,
        source_node_id=source_node_id,
        source_pressure_bar=source_pressure_bar,
        min_required_pressure_bar=min_required_pressure_bar,
        max_velocity_m_s=max_velocity_m_s,
        water_temperature_c=water_temperature_c,
    )