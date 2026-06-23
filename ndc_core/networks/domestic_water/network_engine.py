from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.catalogs.singular_loss_catalog import SingularLossCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.domain.networks.network import Network
from ndc_core.hydraulics.conversions import pressure_bar_to_pa
from ndc_core.networks.domestic_water.pressure_loss import (
    DomesticWaterPressureLossResult,
    compute_cold_water_section_pressure_loss,
    compute_hot_water_section_pressure_loss,
)
from ndc_core.networks.domestic_water.pressure_network import (
    DomesticWaterPressureNetworkEngine,
    DomesticWaterPressurePropagationResult,
    DomesticWaterPressureSummary,
)
from ndc_core.networks.domestic_water.section_sizing import (
    DomesticWaterSectionSizing,
    size_cold_water_section_from_counts,
    size_hot_water_section_from_counts,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


class DomesticWaterNetworkStep(StrEnum):
    """Network compute step names."""

    SIZING = "sizing"
    PRESSURE_LOSS = "pressure_loss"
    PRESSURE_PROPAGATION = "pressure_propagation"
    PRESSURE_SUMMARY = "pressure_summary"


@dataclass(frozen=True, slots=True)
class DomesticWaterSectionComputeResult:
    """Consolidated compute result for one section."""

    section_id: str
    sizing: DomesticWaterSectionSizing | None = None
    pressure_loss: DomesticWaterPressureLossResult | None = None
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @property
    def sizing_ok(self) -> bool:
        return self.sizing is not None and not self.sizing.has_errors

    @property
    def pressure_loss_ok(self) -> bool:
        return self.pressure_loss is not None and not self.pressure_loss.has_errors

    @property
    def has_pressure_loss(self) -> bool:
        return self.pressure_loss is not None

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)


@dataclass(frozen=True, slots=True)
class DomesticWaterNetworkComputeResult:
    """Consolidated network compute result."""

    side: DomesticWaterSide
    section_results: dict[str, DomesticWaterSectionComputeResult]
    pressure_propagation: DomesticWaterPressurePropagationResult | None = None
    pressure_summary: DomesticWaterPressureSummary | None = None
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @property
    def section_count(self) -> int:
        return len(self.section_results)

    @property
    def sized_section_count(self) -> int:
        return sum(1 for result in self.section_results.values() if result.sizing_ok)

    @property
    def pressure_loss_section_count(self) -> int:
        return sum(
            1
            for result in self.section_results.values()
            if result.pressure_loss_ok
        )

    @property
    def has_pressure_propagation(self) -> bool:
        return self.pressure_propagation is not None

    @property
    def has_pressure_summary(self) -> bool:
        return self.pressure_summary is not None

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)


@dataclass(frozen=True, slots=True)
class DomesticWaterNetworkEngine:
    """
    Common EFS/ECS network orchestration engine.

    This class does not own hydraulic formulas. It coordinates:
    - section demand/sizing;
    - section pressure losses;
    - network pressure propagation;
    - worst terminal pressure summary.
    """

    nodes: Mapping[str, Any]
    sections: Mapping[str, Any]
    appliance_catalog: ApplianceCatalog
    pipe_catalog: PipeCatalog
    fluid_catalog: FluidCatalog
    singular_loss_catalog: SingularLossCatalog | None = None
    side: DomesticWaterSide = DomesticWaterSide.COLD_WATER

    @classmethod
    def cold_water(
        cls,
        *,
        nodes: Mapping[str, Any],
        sections: Mapping[str, Any],
        appliance_catalog: ApplianceCatalog,
        pipe_catalog: PipeCatalog,
        fluid_catalog: FluidCatalog,
        singular_loss_catalog: SingularLossCatalog | None = None,
    ) -> DomesticWaterNetworkEngine:
        return cls(
            nodes=nodes,
            sections=sections,
            appliance_catalog=appliance_catalog,
            pipe_catalog=pipe_catalog,
            fluid_catalog=fluid_catalog,
            singular_loss_catalog=singular_loss_catalog,
            side=DomesticWaterSide.COLD_WATER,
        )

    @classmethod
    def hot_water(
        cls,
        *,
        nodes: Mapping[str, Any],
        sections: Mapping[str, Any],
        appliance_catalog: ApplianceCatalog,
        pipe_catalog: PipeCatalog,
        fluid_catalog: FluidCatalog,
        singular_loss_catalog: SingularLossCatalog | None = None,
    ) -> DomesticWaterNetworkEngine:
        return cls(
            nodes=nodes,
            sections=sections,
            appliance_catalog=appliance_catalog,
            pipe_catalog=pipe_catalog,
            fluid_catalog=fluid_catalog,
            singular_loss_catalog=singular_loss_catalog,
            side=DomesticWaterSide.HOT_WATER,
        )

    @classmethod
    def from_network(
        cls,
        *,
        network: Network,
        appliance_catalog: ApplianceCatalog,
        pipe_catalog: PipeCatalog,
        fluid_catalog: FluidCatalog,
        singular_loss_catalog: SingularLossCatalog | None = None,
        side: DomesticWaterSide = DomesticWaterSide.COLD_WATER,
    ) -> DomesticWaterNetworkEngine:
        """
        Build a domestic water engine from the domain Network object.

        This is the preferred entry point for GUI/export layers because they
        should manipulate the business aggregate, not raw node/section mappings.
        """

        return cls(
            nodes=network.nodes,
            sections=network.sections,
            appliance_catalog=appliance_catalog,
            pipe_catalog=pipe_catalog,
            fluid_catalog=fluid_catalog,
            singular_loss_catalog=singular_loss_catalog,
            side=side,
        )

    @classmethod
    def cold_water_from_network(
        cls,
        *,
        network: Network,
        appliance_catalog: ApplianceCatalog,
        pipe_catalog: PipeCatalog,
        fluid_catalog: FluidCatalog,
        singular_loss_catalog: SingularLossCatalog | None = None,
    ) -> DomesticWaterNetworkEngine:
        return cls.from_network(
            network=network,
            appliance_catalog=appliance_catalog,
            pipe_catalog=pipe_catalog,
            fluid_catalog=fluid_catalog,
            singular_loss_catalog=singular_loss_catalog,
            side=DomesticWaterSide.COLD_WATER,
        )

    @classmethod
    def hot_water_from_network(
        cls,
        *,
        network: Network,
        appliance_catalog: ApplianceCatalog,
        pipe_catalog: PipeCatalog,
        fluid_catalog: FluidCatalog,
        singular_loss_catalog: SingularLossCatalog | None = None,
    ) -> DomesticWaterNetworkEngine:
        return cls.from_network(
            network=network,
            appliance_catalog=appliance_catalog,
            pipe_catalog=pipe_catalog,
            fluid_catalog=fluid_catalog,
            singular_loss_catalog=singular_loss_catalog,
            side=DomesticWaterSide.HOT_WATER,
        )

    def compute_sections(
        self,
        *,
        max_velocity_m_s: float | None = None,
        water_temperature_c: float | None = None,
    ) -> Result[DomesticWaterNetworkComputeResult]:
        """
        Compute sizing and pressure losses for all sections matching the engine side.
        """

        messages: list[EngineMessage] = []
        section_results: dict[str, DomesticWaterSectionComputeResult] = {}

        for section_id, section in self.sections.items():
            if not _section_matches_side(section, self.side):
                continue

            section_result = self._compute_one_section(
                section_id=str(section_id),
                section=section,
                max_velocity_m_s=max_velocity_m_s,
                water_temperature_c=water_temperature_c,
            )

            section_results[str(section_id)] = section_result
            messages.extend(section_result.messages)

        result = DomesticWaterNetworkComputeResult(
            side=self.side,
            section_results=section_results,
            messages=tuple(messages),
        )

        if result.has_errors:
            return Result.failure(value=result, messages=messages)

        if result.has_warnings:
            return Result.partial(value=result, messages=messages)

        return Result.success(value=result, messages=messages)

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
        Compute sections, then optionally propagate pressure and summarize terminals.

        Pressure propagation is executed only when both source_node_id and
        source_pressure_bar are provided.
        """

        messages: list[EngineMessage] = []

        sections_result = self.compute_sections(
            max_velocity_m_s=max_velocity_m_s,
            water_temperature_c=water_temperature_c,
        )
        messages.extend(sections_result.messages)

        if sections_result.value is None:
            return Result.failure(messages=messages)

        pressure_propagation: DomesticWaterPressurePropagationResult | None = None
        pressure_summary: DomesticWaterPressureSummary | None = None

        if source_node_id is not None and source_pressure_bar is not None:
            pressure_engine = DomesticWaterPressureNetworkEngine(
                nodes=self.nodes,
                sections=self.sections,
                side=self.side,
            )

            propagation_result = pressure_engine.propagate_pressures(
                source_node_id=source_node_id,
                source_pressure_pa=pressure_bar_to_pa(source_pressure_bar),
            )
            messages.extend(propagation_result.messages)
            pressure_propagation = propagation_result.value

            summary_result = pressure_engine.summarize_worst_terminal_pressure(
                source_node_id=source_node_id,
                source_pressure_bar=source_pressure_bar,
                min_required_pressure_bar=min_required_pressure_bar,
            )
            messages.extend(summary_result.messages)
            pressure_summary = summary_result.value

        result = DomesticWaterNetworkComputeResult(
            side=self.side,
            section_results=sections_result.value.section_results,
            pressure_propagation=pressure_propagation,
            pressure_summary=pressure_summary,
            messages=tuple(messages),
        )

        if result.has_errors:
            return Result.failure(value=result, messages=messages)

        if result.has_warnings:
            return Result.partial(value=result, messages=messages)

        return Result.success(value=result, messages=messages)

    def _compute_one_section(
        self,
        *,
        section_id: str,
        section: Any,
        max_velocity_m_s: float | None,
        water_temperature_c: float | None,
    ) -> DomesticWaterSectionComputeResult:
        messages: list[EngineMessage] = []

        appliance_counts = _read_section_downstream_appliance_counts(section)
        if not appliance_counts:
            messages.append(
                EngineMessage.warning(
                    code="DOMESTIC_WATER_NETWORK_SECTION_NO_APPLIANCES",
                    text="Section has no downstream appliance counts.",
                    context={
                        "section_id": section_id,
                        "step": DomesticWaterNetworkStep.SIZING.value,
                    },
                )
            )

        sizing_result = self._size_section(
            section=section,
            appliance_counts=appliance_counts,
            max_velocity_m_s=max_velocity_m_s,
        )
        messages.extend(sizing_result.messages)

        sizing = sizing_result.value

        if sizing is None or sizing.has_errors:
            return DomesticWaterSectionComputeResult(
                section_id=section_id,
                sizing=sizing,
                pressure_loss=None,
                messages=tuple(messages),
            )

        if getattr(section, "selected_internal_diameter_mm", None) is None:
            messages.append(
                EngineMessage.warning(
                    code="DOMESTIC_WATER_NETWORK_SECTION_NOT_SIZED",
                    text=(
                        "Section has no selected internal diameter after sizing; "
                        "pressure loss was skipped."
                    ),
                    context={
                        "section_id": section_id,
                        "step": DomesticWaterNetworkStep.PRESSURE_LOSS.value,
                    },
                )
            )
            return DomesticWaterSectionComputeResult(
                section_id=section_id,
                sizing=sizing,
                pressure_loss=None,
                messages=tuple(messages),
            )

        pressure_loss_result = self._compute_section_pressure_loss(
            section=section,
            water_temperature_c=water_temperature_c,
        )
        messages.extend(pressure_loss_result.messages)

        return DomesticWaterSectionComputeResult(
            section_id=section_id,
            sizing=sizing,
            pressure_loss=pressure_loss_result.value,
            messages=tuple(messages),
        )

    def _size_section(
        self,
        *,
        section: Any,
        appliance_counts: Mapping[str, int],
        max_velocity_m_s: float | None,
    ) -> Result[DomesticWaterSectionSizing]:
        if self.side is DomesticWaterSide.HOT_WATER:
            return size_hot_water_section_from_counts(
                section=section,
                appliance_counts=appliance_counts,
                appliance_catalog=self.appliance_catalog,
                pipe_catalog=self.pipe_catalog,
                max_velocity_m_s=max_velocity_m_s,
            )

        return size_cold_water_section_from_counts(
            section=section,
            appliance_counts=appliance_counts,
            appliance_catalog=self.appliance_catalog,
            pipe_catalog=self.pipe_catalog,
            max_velocity_m_s=max_velocity_m_s,
        )

    def _compute_section_pressure_loss(
        self,
        *,
        section: Any,
        water_temperature_c: float | None,
    ) -> Result[DomesticWaterPressureLossResult]:
        if self.side is DomesticWaterSide.HOT_WATER:
            return compute_hot_water_section_pressure_loss(
                section=section,
                fluid_catalog=self.fluid_catalog,
                pipe_catalog=self.pipe_catalog,
                singular_loss_catalog=self.singular_loss_catalog,
                water_temperature_c=water_temperature_c,
            )

        return compute_cold_water_section_pressure_loss(
            section=section,
            fluid_catalog=self.fluid_catalog,
            pipe_catalog=self.pipe_catalog,
            singular_loss_catalog=self.singular_loss_catalog,
            water_temperature_c=water_temperature_c,
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
    """Convenience function for full EFS network computation."""

    return DomesticWaterNetworkEngine.cold_water(
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
    """Convenience function for full ECS forward network computation."""

    return DomesticWaterNetworkEngine.hot_water(
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


def compute_cold_water_network_from_domain(
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
    """Convenience function for full EFS computation from a domain Network."""

    return DomesticWaterNetworkEngine.cold_water_from_network(
        network=network,
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


def compute_hot_water_network_from_domain(
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
    """Convenience function for full ECS forward computation from a domain Network."""

    return DomesticWaterNetworkEngine.hot_water_from_network(
        network=network,
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


def _read_section_downstream_appliance_counts(section: Any) -> dict[str, int]:
    raw_counts = getattr(section, "downstream_appliance_counts", None) or {}
    normalized: dict[str, int] = {}

    for raw_code, raw_count in raw_counts.items():
        code = str(raw_code or "").strip()
        if not code:
            continue

        try:
            count = int(raw_count)
        except (TypeError, ValueError):
            continue

        if count <= 0:
            continue

        normalized[code] = normalized.get(code, 0) + count

    return normalized


def _section_matches_side(section: Any, side: DomesticWaterSide) -> bool:
    fluid_code = str(getattr(section, "fluid_code", "") or "").strip().lower()

    if side is DomesticWaterSide.HOT_WATER:
        return fluid_code in {"ecs", "hot_water", "hot water", "domestic_hot_water"}

    return fluid_code in {"efs", "cold_water", "cold water", "domestic_cold_water"}