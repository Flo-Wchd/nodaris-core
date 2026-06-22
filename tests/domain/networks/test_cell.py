from ndc_core.domain.networks.cell import Cell


def test_cell_normalizes_identity() -> None:
    cell = Cell(id=" C1 ", name=" Appartement 101 ")

    assert cell.id == "C1"
    assert cell.name == "Appartement 101"


def test_cell_set_appliance_count() -> None:
    cell = Cell(id="C1", name="Cell")

    cell.set_appliance_count("lavabo", 2)

    assert cell.get_appliance_count("lavabo") == 2
    assert cell.has_appliances
    assert cell.total_appliance_count == 2


def test_cell_removes_appliance_when_count_is_zero() -> None:
    cell = Cell(id="C1", name="Cell", appliance_counts={"lavabo": 2})

    cell.set_appliance_count("lavabo", 0)

    assert cell.get_appliance_count("lavabo") == 0
    assert not cell.has_appliances


def test_cell_add_appliance_count() -> None:
    cell = Cell(id="C1", name="Cell")

    cell.add_appliance_count("lavabo")
    cell.add_appliance_count("lavabo", 2)

    assert cell.get_appliance_count("lavabo") == 3


def test_cell_copy_appliance_counts_is_independent() -> None:
    cell = Cell(id="C1", name="Cell", appliance_counts={"lavabo": 1})

    counts = cell.copy_appliance_counts()
    counts["lavabo"] = 99

    assert cell.get_appliance_count("lavabo") == 1