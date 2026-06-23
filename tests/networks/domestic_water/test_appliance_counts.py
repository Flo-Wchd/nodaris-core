from __future__ import annotations

from ndc_core.networks.domestic_water.appliance_counts import (
    apply_machine_exclusivity,
    merge_appliance_counts,
    normalize_appliance_counts,
)


def test_normalize_appliance_counts_ignores_invalid_values() -> None:
    assert normalize_appliance_counts(
        {
            "L": 1,
            "D": "2",
            "WC": 0,
            "BAD": -1,
            "": 4,
            None: 5,
            "INVALID": "abc",
        }
    ) == {
        "L": 1,
        "D": 2,
    }


def test_normalize_appliance_counts_merges_duplicate_codes() -> None:
    assert normalize_appliance_counts(
        {
            "L": 1,
            " L ": 2,
            "D": 1,
        }
    ) == {
        "L": 3,
        "D": 1,
    }


def test_normalize_appliance_counts_accepts_non_mapping_input() -> None:
    assert normalize_appliance_counts(None) == {}
    assert normalize_appliance_counts([]) == {}
    assert normalize_appliance_counts("L") == {}


def test_merge_appliance_counts() -> None:
    assert merge_appliance_counts(
        {"L": 1, "D": 1},
        {"L": 2, "WC": 0},
        {"WC": 1},
    ) == {
        "L": 3,
        "D": 1,
        "WC": 1,
    }


def test_apply_machine_exclusivity_counts_ll_lv_as_one() -> None:
    result = apply_machine_exclusivity(
        {
            "LL": 1,
            "LV": 1,
            "L": 1,
        },
        exclusive_codes={"LL", "LV"},
    )

    assert result == {
        "L": 1,
        "LL": 1,
    }


def test_apply_machine_exclusivity_keeps_single_machine() -> None:
    result = apply_machine_exclusivity(
        {
            "LL": 1,
            "L": 1,
        },
        exclusive_codes={"LL", "LV"},
    )

    assert result == {
        "LL": 1,
        "L": 1,
    }


def test_apply_machine_exclusivity_is_case_insensitive() -> None:
    result = apply_machine_exclusivity(
        {
            "ll": 1,
            "lv": 1,
            "L": 1,
        },
        exclusive_codes={"LL", "LV"},
    )

    assert result == {
        "L": 1,
        "ll": 1,
    }