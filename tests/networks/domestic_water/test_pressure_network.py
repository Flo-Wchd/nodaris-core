from __future__ import annotations

from dataclasses import dataclass, field

from ndc_core.networks.domestic_water.pressure_network import (
    DomesticWaterPressureNetworkEngine,
    PressurePropagationStatus,
    PressureSummaryStatus,
    propagate_cold_water_pressures,
    summarize_cold_water_worst_terminal_pressure,
)


@dataclass
class _Node:
    id: str
    downstream_section_ids: list[str] = field(default_factory=list)
    pressure_pa: float | None = None


@dataclass
class _Section:
    id: str
    upstream_node_id: str
    downstream_node_id: str
    fluid_code: str = "EFS"
    total_pressure_loss_pa: float | None = None
    pressure_start_pa: float | None = None
    pressure_end_pa: float | None = None


def test_propagate_pressures_on_simple_network() -> None:
    nodes = {
        "A": _Node(id="A", downstream_section_ids=["S1"]),
        "B": _Node(id="B", downstream_section_ids=[]),
    }
    sections = {
        "S1": _Section(
            id="S1",
            upstream_node_id="A",
            downstream_node_id="B",
            total_pressure_loss_pa=25_000.0,
        ),
    }

    result = propagate_cold_water_pressures(
        nodes=nodes,
        sections=sections,
        source_node_id="A",
        source_pressure_pa=300_000.0,
    )

    assert result.ok
    assert result.value is not None

    pressures = result.value.node_pressures

    assert pressures["A"].pressure_pa == 300_000.0
    assert pressures["B"].pressure_pa == 275_000.0

    assert nodes["A"].pressure_pa == 300_000.0
    assert nodes["B"].pressure_pa == 275_000.0

    assert sections["S1"].pressure_start_pa == 300_000.0
    assert sections["S1"].pressure_end_pa == 275_000.0


def test_branching_keeps_most_unfavorable_pressure_on_merge() -> None:
    nodes = {
        "A": _Node(id="A", downstream_section_ids=["S1", "S2"]),
        "B": _Node(id="B", downstream_section_ids=["S3"]),
        "D": _Node(id="D", downstream_section_ids=["S4"]),
        "C": _Node(id="C", downstream_section_ids=[]),
    }
    sections = {
        "S1": _Section(
            id="S1",
            upstream_node_id="A",
            downstream_node_id="B",
            total_pressure_loss_pa=10.0,
        ),
        "S3": _Section(
            id="S3",
            upstream_node_id="B",
            downstream_node_id="C",
            total_pressure_loss_pa=10.0,
        ),
        "S2": _Section(
            id="S2",
            upstream_node_id="A",
            downstream_node_id="D",
            total_pressure_loss_pa=50.0,
        ),
        "S4": _Section(
            id="S4",
            upstream_node_id="D",
            downstream_node_id="C",
            total_pressure_loss_pa=1.0,
        ),
    }

    engine = DomesticWaterPressureNetworkEngine(nodes=nodes, sections=sections)

    result = engine.propagate_pressures(
        source_node_id="A",
        source_pressure_pa=100.0,
    )

    assert result.ok
    assert result.value is not None

    pressures = result.value.node_pressures

    assert pressures["A"].pressure_pa == 100.0
    assert pressures["B"].pressure_pa == 90.0
    assert pressures["D"].pressure_pa == 50.0
    assert pressures["C"].pressure_pa == 49.0


def test_negative_pressure_loss_increases_downstream_pressure() -> None:
    nodes = {
        "A": _Node(id="A", downstream_section_ids=["S1"]),
        "B": _Node(id="B", downstream_section_ids=[]),
    }
    sections = {
        "S1": _Section(
            id="S1",
            upstream_node_id="A",
            downstream_node_id="B",
            total_pressure_loss_pa=-20.0,
        ),
    }

    result = propagate_cold_water_pressures(
        nodes=nodes,
        sections=sections,
        source_node_id="A",
        source_pressure_pa=100.0,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.node_pressures["B"].pressure_pa == 120.0


def test_missing_pressure_loss_warns_and_uses_zero_delta_p() -> None:
    nodes = {
        "A": _Node(id="A", downstream_section_ids=["S1"]),
        "B": _Node(id="B", downstream_section_ids=[]),
    }
    sections = {
        "S1": _Section(
            id="S1",
            upstream_node_id="A",
            downstream_node_id="B",
            total_pressure_loss_pa=None,
        ),
    }

    result = propagate_cold_water_pressures(
        nodes=nodes,
        sections=sections,
        source_node_id="A",
        source_pressure_pa=123.0,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.node_pressures["B"].pressure_pa == 123.0
    assert result.value.has_warnings
    assert any(
        message.code == "DOMESTIC_WATER_PRESSURE_LOSS_MISSING"
        for message in result.value.messages
    )


def test_unknown_source_returns_failure() -> None:
    result = propagate_cold_water_pressures(
        nodes={},
        sections={},
        source_node_id="UNKNOWN",
        source_pressure_pa=100.0,
    )

    assert result.failed
    assert result.value is not None
    assert result.value.status is PressurePropagationStatus.SOURCE_NOT_FOUND
    assert any(
        message.code == "DOMESTIC_WATER_PRESSURE_SOURCE_NOT_FOUND"
        for message in result.messages
    )


def test_worst_terminal_summary() -> None:
    nodes = {
        "A": _Node(id="A", downstream_section_ids=["S1", "S2"]),
        "B": _Node(id="B", downstream_section_ids=["S3"]),
        "D": _Node(id="D", downstream_section_ids=["S4"]),
        "C": _Node(id="C", downstream_section_ids=[]),
    }
    sections = {
        "S1": _Section(
            id="S1",
            upstream_node_id="A",
            downstream_node_id="B",
            total_pressure_loss_pa=0.10 * 100_000.0,
        ),
        "S3": _Section(
            id="S3",
            upstream_node_id="B",
            downstream_node_id="C",
            total_pressure_loss_pa=0.10 * 100_000.0,
        ),
        "S2": _Section(
            id="S2",
            upstream_node_id="A",
            downstream_node_id="D",
            total_pressure_loss_pa=0.50 * 100_000.0,
        ),
        "S4": _Section(
            id="S4",
            upstream_node_id="D",
            downstream_node_id="C",
            total_pressure_loss_pa=0.01 * 100_000.0,
        ),
    }

    result = summarize_cold_water_worst_terminal_pressure(
        nodes=nodes,
        sections=sections,
        source_node_id="A",
        source_pressure_bar=3.0,
        min_required_pressure_bar=2.6,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.worst_terminal is not None

    worst = result.value.worst_terminal

    assert result.value.status is PressureSummaryStatus.INSUFFICIENT_PRESSURE
    assert result.value.has_insufficient_pressure
    assert not result.value.is_ok
    assert result.value.terminal_count == 1
    assert result.value.critical_node_id == "C"
    assert result.value.worst_pressure_bar == 2.49
    assert round(result.value.pressure_margin_bar or 0.0, 2) == -0.11

    assert worst.node_id == "C"
    assert worst.pressure_bar == 2.49
    assert round(worst.delta_to_min_bar, 2) == -0.11
    assert worst.is_below_min
    assert set(result.value.terminal_statuses) == {"C"}


def test_hot_water_sections_are_ignored_by_cold_water_engine() -> None:
    nodes = {
        "A": _Node(id="A", downstream_section_ids=["S1"]),
        "B": _Node(id="B", downstream_section_ids=[]),
    }
    sections = {
        "S1": _Section(
            id="S1",
            upstream_node_id="A",
            downstream_node_id="B",
            fluid_code="ECS",
            total_pressure_loss_pa=50.0,
        ),
    }

    result = propagate_cold_water_pressures(
        nodes=nodes,
        sections=sections,
        source_node_id="A",
        source_pressure_pa=100.0,
    )

    assert result.ok
    assert result.value is not None
    assert set(result.value.node_pressures) == {"A"}


def test_worst_terminal_summary_ok_status() -> None:
    nodes = {
        "A": _Node(id="A", downstream_section_ids=["S1"]),
        "B": _Node(id="B", downstream_section_ids=[]),
    }
    sections = {
        "S1": _Section(
            id="S1",
            upstream_node_id="A",
            downstream_node_id="B",
            total_pressure_loss_pa=0.25 * 100_000.0,
        ),
    }

    result = summarize_cold_water_worst_terminal_pressure(
        nodes=nodes,
        sections=sections,
        source_node_id="A",
        source_pressure_bar=3.0,
        min_required_pressure_bar=2.5,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.status is PressureSummaryStatus.OK
    assert result.value.is_ok
    assert not result.value.has_insufficient_pressure
    assert result.value.terminal_count == 1
    assert result.value.critical_node_id == "B"
    assert result.value.worst_pressure_bar == 2.75
    assert result.value.pressure_margin_bar == 0.25


def test_worst_terminal_summary_no_terminal_status() -> None:
    nodes = {
        "A": _Node(id="A", downstream_section_ids=["S1"]),
        "B": _Node(id="B", downstream_section_ids=["S2"]),
        "C": _Node(id="C", downstream_section_ids=["S3"]),
    }
    sections = {
        "S1": _Section(
            id="S1",
            upstream_node_id="A",
            downstream_node_id="B",
            total_pressure_loss_pa=10.0,
        ),
        "S2": _Section(
            id="S2",
            upstream_node_id="B",
            downstream_node_id="C",
            total_pressure_loss_pa=10.0,
        ),
        "S3": _Section(
            id="S3",
            upstream_node_id="C",
            downstream_node_id="A",
            total_pressure_loss_pa=10.0,
        ),
    }

    result = summarize_cold_water_worst_terminal_pressure(
        nodes=nodes,
        sections=sections,
        source_node_id="A",
        source_pressure_bar=3.0,
        min_required_pressure_bar=1.0,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.status is PressureSummaryStatus.NO_TERMINAL_REACHED
    assert not result.value.has_worst_terminal
    assert result.value.terminal_count == 0
    assert result.value.critical_node_id is None
    assert result.value.worst_pressure_bar is None
    assert result.value.pressure_margin_bar is None
    assert result.value.has_warnings


def test_worst_terminal_summary_source_not_found_status() -> None:
    result = summarize_cold_water_worst_terminal_pressure(
        nodes={},
        sections={},
        source_node_id="UNKNOWN",
        source_pressure_bar=3.0,
        min_required_pressure_bar=1.0,
    )

    assert result.failed
    assert result.value is not None
    assert result.value.status is PressureSummaryStatus.SOURCE_NOT_FOUND
    assert not result.value.has_worst_terminal
    assert result.value.terminal_count == 0
    assert result.value.propagation.status is PressurePropagationStatus.SOURCE_NOT_FOUND