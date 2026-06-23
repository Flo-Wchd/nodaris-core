from __future__ import annotations

from dataclasses import dataclass, field

from ndc_core.networks.domestic_water.entity_access import (
    apply_node_pressures,
    apply_section_pressures,
    clean_entity_id,
    clean_optional_code,
    read_downstream_section_ids,
    write_node_downstream_appliance_counts,
    write_section_downstream_appliance_counts,
    read_cell_appliance_counts,
    read_node_local_appliance_counts,
)


@dataclass
class _Node:
    downstream_section_ids: list[object] = field(default_factory=list)
    downstream_appliance_counts: dict[str, int] = field(default_factory=dict)
    appliance_counts: dict[str, int] = field(default_factory=dict)
    appliances: dict[str, int] = field(default_factory=dict)
    cells: list[object] = field(default_factory=list)
    pressure_pa: float | None = None

@dataclass
class _Section:
    downstream_appliance_counts: dict[str, int] = field(default_factory=dict)
    pressure_start_pa: float | None = None
    pressure_end_pa: float | None = None


@dataclass
class _Cell:
    appliance_counts: dict[str, int] = field(default_factory=dict)
    appliances: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class _NodeState:
    pressure_pa: float


def test_clean_entity_id() -> None:
    assert clean_entity_id(" S1 ") == "S1"
    assert clean_entity_id(None) == ""
    assert clean_entity_id(12) == "12"


def test_clean_optional_code() -> None:
    assert clean_optional_code(" P20 ") == "P20"
    assert clean_optional_code(None) is None
    assert clean_optional_code("") is None


def test_read_downstream_section_ids() -> None:
    node = _Node(downstream_section_ids=[" S1 ", "", None, "S2"])

    assert read_downstream_section_ids(node) == ("S1", "S2")


def test_write_section_downstream_appliance_counts() -> None:
    section = _Section(downstream_appliance_counts={"OLD": 1})

    write_section_downstream_appliance_counts(
        section,
        {
            "L": 1,
            "D": "2",
            "BAD": 0,
        },
    )

    assert section.downstream_appliance_counts == {"L": 1, "D": 2}


def test_write_node_downstream_appliance_counts() -> None:
    node = _Node(downstream_appliance_counts={"OLD": 1})

    write_node_downstream_appliance_counts(
        node,
        {
            "L": 1,
            "D": "2",
            "BAD": -1,
        },
    )

    assert node.downstream_appliance_counts == {"L": 1, "D": 2}


def test_apply_section_pressures() -> None:
    section = _Section()

    apply_section_pressures(
        section=section,
        pressure_start_pa=300_000.0,
        pressure_end_pa=275_000.0,
    )

    assert section.pressure_start_pa == 300_000.0
    assert section.pressure_end_pa == 275_000.0


def test_apply_node_pressures() -> None:
    nodes = {
        "N0": _Node(),
        "N1": _Node(),
    }
    node_states = {
        "N0": _NodeState(pressure_pa=300_000.0),
        "N1": _NodeState(pressure_pa=275_000.0),
        "UNKNOWN": _NodeState(pressure_pa=1.0),
    }

    apply_node_pressures(nodes, node_states)

    assert nodes["N0"].pressure_pa == 300_000.0
    assert nodes["N1"].pressure_pa == 275_000.0


def test_read_cell_appliance_counts() -> None:
    cell = _Cell(
        appliance_counts={
            "L": 1,
            "D": "2",
            "BAD": 0,
        },
    )

    assert read_cell_appliance_counts(cell) == {"L": 1, "D": 2}


def test_read_node_local_appliance_counts_from_method() -> None:
    class NodeWithMethod:
        def local_appliance_counts(self) -> dict[str, object]:
            return {
                "L": 1,
                "D": "2",
                "BAD": 0,
            }

    assert read_node_local_appliance_counts(NodeWithMethod()) == {
        "L": 1,
        "D": 2,
    }


def test_read_node_local_appliance_counts_from_attributes_and_cells() -> None:
    node = _Node(
        appliance_counts={"L": 1},
        appliances={"D": 1},
        cells=[
            _Cell(appliance_counts={"WC": 1}),
            _Cell(appliances={"LL": 1}),
        ],
    )

    assert read_node_local_appliance_counts(node) == {
        "L": 1,
        "D": 1,
        "WC": 1,
        "LL": 1,
    }


def test_read_node_local_appliance_counts_handles_invalid_method() -> None:
    class NodeWithInvalidMethod:
        def local_appliance_counts(self) -> None:
            raise TypeError("invalid")

    assert read_node_local_appliance_counts(NodeWithInvalidMethod()) == {}