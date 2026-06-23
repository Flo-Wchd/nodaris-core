from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.networks.domestic_water.types import DomesticWaterSide
from ndc_core.networks.domestic_water.side_matching import (
    section_matches_domestic_water_side,
)
from ndc_core.networks.domestic_water.appliance_counts import (
    merge_appliance_counts,
    normalize_appliance_counts,
)


@dataclass(frozen=True, slots=True)
class DomesticWaterAppliancePropagationResult:
    """
    Result of automatic Cell -> Node -> Section appliance propagation.

    The propagation is intentionally limited to appliance count maps. It does not:
    - compute DTU demand;
    - apply simultaneity;
    - size pipes;
    - compute pressure losses.

    For each section, downstream_appliance_counts represents all appliances
    located downstream of that section.
    """

    side: DomesticWaterSide
    node_local_counts: dict[str, dict[str, int]]
    node_downstream_counts: dict[str, dict[str, int]]
    section_downstream_counts: dict[str, dict[str, int]]
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)
    propagated: bool = False

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)

    @property
    def propagated_section_count(self) -> int:
        return len(self.section_downstream_counts)


@dataclass(frozen=True, slots=True)
class DomesticWaterAppliancePropagationEngine:
    """
    Propagate local appliances from nodes/cells to downstream section counts.

    Graph convention:
        section.upstream_node_id -> section.downstream_node_id

    For a section U -> D:
        section.downstream_appliance_counts = all local appliances attached to D
        and all appliances further downstream of D.

    Existing manual section.downstream_appliance_counts are preserved when the
    network has no local appliance demand on nodes/cells. This keeps manual/test
    workflows valid while enabling the future GUI workflow based on Cell -> Node.
    """

    nodes: Mapping[str, Any]
    sections: Mapping[str, Any]
    side: DomesticWaterSide = DomesticWaterSide.COLD_WATER

    def propagate(self) -> Result[DomesticWaterAppliancePropagationResult]:
        messages: list[EngineMessage] = []

        node_local_counts = {
            str(node_id): _read_node_local_appliance_counts(node)
            for node_id, node in self.nodes.items()
        }

        has_local_demand = any(bool(counts) for counts in node_local_counts.values())

        if not has_local_demand:
            result = DomesticWaterAppliancePropagationResult(
                side=self.side,
                node_local_counts=node_local_counts,
                node_downstream_counts={},
                section_downstream_counts={},
                messages=tuple(messages),
                propagated=False,
            )
            return Result.success(value=result, messages=messages)

        children_by_node: dict[str, list[tuple[str, str]]] = defaultdict(list)

        for section_id, section in self.sections.items():
            section_id_s = str(section_id)

            if not section_matches_domestic_water_side(section, self.side):
                continue

            upstream_node_id = _clean_id(getattr(section, "upstream_node_id", None))
            downstream_node_id = _clean_id(getattr(section, "downstream_node_id", None))

            if not upstream_node_id or not downstream_node_id:
                messages.append(
                    EngineMessage.warning(
                        code="DOMESTIC_WATER_APPLIANCE_SECTION_TOPOLOGY_INCOMPLETE",
                        text=(
                            "Section has incomplete topology; appliance propagation "
                            "was skipped for this section."
                        ),
                        context={
                            "section_id": section_id_s,
                            "upstream_node_id": upstream_node_id,
                            "downstream_node_id": downstream_node_id,
                        },
                    )
                )
                continue

            if upstream_node_id not in self.nodes:
                messages.append(
                    EngineMessage.warning(
                        code="DOMESTIC_WATER_APPLIANCE_UPSTREAM_NODE_NOT_FOUND",
                        text=(
                            "Section upstream node was not found during appliance "
                            "propagation."
                        ),
                        context={
                            "section_id": section_id_s,
                            "upstream_node_id": upstream_node_id,
                        },
                    )
                )

            if downstream_node_id not in self.nodes:
                messages.append(
                    EngineMessage.warning(
                        code="DOMESTIC_WATER_APPLIANCE_DOWNSTREAM_NODE_NOT_FOUND",
                        text=(
                            "Section downstream node was not found during appliance "
                            "propagation."
                        ),
                        context={
                            "section_id": section_id_s,
                            "downstream_node_id": downstream_node_id,
                        },
                    )
                )

            children_by_node[upstream_node_id].append(
                (section_id_s, downstream_node_id)
            )

        node_downstream_counts: dict[str, dict[str, int]] = {}
        section_downstream_counts: dict[str, dict[str, int]] = {}
        visiting: set[str] = set()
        cycle_reported: set[str] = set()

        def compute_node_downstream_counts(node_id: str) -> dict[str, int]:
            if node_id in node_downstream_counts:
                return dict(node_downstream_counts[node_id])

            if node_id in visiting:
                if node_id not in cycle_reported:
                    messages.append(
                        EngineMessage.error(
                            code="DOMESTIC_WATER_APPLIANCE_GRAPH_CYCLE",
                            text=(
                                "Cycle detected in domestic water network topology; "
                                "appliance propagation returned a best-effort result."
                            ),
                            context={"node_id": node_id},
                        )
                    )
                    cycle_reported.add(node_id)

                return dict(node_local_counts.get(node_id, {}))

            visiting.add(node_id)

            total_counts = dict(node_local_counts.get(node_id, {}))

            for section_id, downstream_node_id in children_by_node.get(node_id, []):
                downstream_counts = compute_node_downstream_counts(downstream_node_id)
                section_downstream_counts[section_id] = dict(downstream_counts)

                section = self.sections.get(section_id)
                if section is not None:
                    _write_section_downstream_counts(section, downstream_counts)

                total_counts = merge_appliance_counts(total_counts, downstream_counts)

            visiting.remove(node_id)

            node_downstream_counts[node_id] = dict(total_counts)

            node = self.nodes.get(node_id)
            if node is not None:
                _write_node_downstream_counts(node, total_counts)

            return dict(total_counts)

        for node_id in self.nodes:
            compute_node_downstream_counts(str(node_id))

        result = DomesticWaterAppliancePropagationResult(
            side=self.side,
            node_local_counts=node_local_counts,
            node_downstream_counts=node_downstream_counts,
            section_downstream_counts=section_downstream_counts,
            messages=tuple(messages),
            propagated=True,
        )

        if result.has_errors:
            return Result.failure(value=result, messages=messages)

        if result.has_warnings:
            return Result.partial(value=result, messages=messages)

        return Result.success(value=result, messages=messages)


def propagate_domestic_water_appliances(
    *,
    nodes: Mapping[str, Any],
    sections: Mapping[str, Any],
    side: DomesticWaterSide = DomesticWaterSide.COLD_WATER,
) -> Result[DomesticWaterAppliancePropagationResult]:
    """
    Convenience function for Cell/Node -> Section appliance propagation.
    """

    return DomesticWaterAppliancePropagationEngine(
        nodes=nodes,
        sections=sections,
        side=side,
    ).propagate()


def propagate_cold_water_appliances(
    *,
    nodes: Mapping[str, Any],
    sections: Mapping[str, Any],
) -> Result[DomesticWaterAppliancePropagationResult]:
    """
    Convenience function for EFS appliance propagation.
    """

    return propagate_domestic_water_appliances(
        nodes=nodes,
        sections=sections,
        side=DomesticWaterSide.COLD_WATER,
    )


def propagate_hot_water_appliances(
    *,
    nodes: Mapping[str, Any],
    sections: Mapping[str, Any],
) -> Result[DomesticWaterAppliancePropagationResult]:
    """
    Convenience function for ECS appliance propagation.
    """

    return propagate_domestic_water_appliances(
        nodes=nodes,
        sections=sections,
        side=DomesticWaterSide.HOT_WATER,
    )


def _read_node_local_appliance_counts(node: Any) -> dict[str, int]:
    if node is None:
        return {}

    local_counts_method = getattr(node, "local_appliance_counts", None)
    if callable(local_counts_method):
        try:
            return normalize_appliance_counts(local_counts_method())
        except (TypeError, ValueError):
            return {}

    merged: dict[str, int] = {}

    for attr_name in ("appliance_counts", "appliances"):
        value = getattr(node, attr_name, None)
        if isinstance(value, dict):
            merged = merge_appliance_counts(merged, normalize_appliance_counts(value))

    cells = getattr(node, "cells", None)
    if isinstance(cells, (list, tuple)):
        for cell in cells:
            merged = merge_appliance_counts(merged, _read_cell_appliance_counts(cell))

    return merged


def _read_cell_appliance_counts(cell: Any) -> dict[str, int]:
    if cell is None:
        return {}

    for attr_name in ("appliance_counts", "appliances"):
        value = getattr(cell, attr_name, None)
        if isinstance(value, dict):
            return normalize_appliance_counts(value)

    return {}


def _write_section_downstream_counts(section: Any, counts: dict[str, int]) -> None:
    normalized = normalize_appliance_counts(counts)

    target = getattr(section, "downstream_appliance_counts", None)
    if isinstance(target, dict):
        target.clear()
        target.update(normalized)
        return

    try:
        setattr(section, "downstream_appliance_counts", dict(normalized))
    except (AttributeError, TypeError):
        return


def _write_node_downstream_counts(node: Any, counts: dict[str, int]) -> None:
    normalized = normalize_appliance_counts(counts)

    target = getattr(node, "downstream_appliance_counts", None)
    if isinstance(target, dict):
        target.clear()
        target.update(normalized)
        return

    try:
        setattr(node, "downstream_appliance_counts", dict(normalized))
    except (AttributeError, TypeError):
        return


def _clean_id(value: Any) -> str:
    return str(value or "").strip()