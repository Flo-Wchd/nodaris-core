from ndc_core.catalogs.appliance_catalog import ApplianceCatalog


def test_appliance_catalog_from_mapping() -> None:
    result = ApplianceCatalog.from_mapping(
        {
            "metadata": {},
            "L": {
                "name": "Lavabo",
                "acronym": "L",
                "cold_design_flow_lps": 0.2,
                "hot_design_flow_lps": 0.2,
                "cold_min_diameter_mm": 10,
                "individual_coefficient": 1.5,
            },
        }
    )

    assert result.ok
    assert result.value is not None

    catalog = result.value
    appliance = catalog.get("l")

    assert appliance is not None
    assert appliance.code == "L"
    assert appliance.name == "Lavabo"
    assert appliance.cold_water_flow_l_s == 0.2
    assert appliance.hot_water_flow_l_s == 0.2
    assert appliance.min_internal_diameter_mm == 10
    assert appliance.individual_coefficient == 1.5


def test_appliance_catalog_ignores_invalid_entries_with_warning() -> None:
    result = ApplianceCatalog.from_mapping({"BAD": []})

    assert result.ok
    assert result.value is not None
    assert result.value.messages[0].code == "APPLIANCE_ENTRY_INVALID"


def test_appliance_catalog_lists_codes() -> None:
    result = ApplianceCatalog.from_mapping(
        {
            "B": {"name": "Baignoire"},
            "L": {"name": "Lavabo"},
        }
    )

    assert result.value is not None
    assert result.value.list_codes() == ["B", "L"]