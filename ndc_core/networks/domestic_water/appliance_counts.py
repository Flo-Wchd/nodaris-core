from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any


def normalize_appliance_counts(raw_counts: Any) -> dict[str, int]:
    """
    Normalize an appliance count mapping.

    Rules:
    - unknown/non-mapping inputs return an empty dict;
    - empty appliance codes are ignored;
    - values are converted to int when possible;
    - zero, negative and invalid values are ignored;
    - duplicate normalized codes are summed.

    This helper is intentionally side-agnostic. EFS/ECS filtering is handled by
    demand/profile logic, not by count normalization.
    """

    if not isinstance(raw_counts, Mapping):
        return {}

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


def merge_appliance_counts(*count_maps: Any) -> dict[str, int]:
    """
    Merge several appliance count mappings using the shared normalization rules.
    """

    merged: dict[str, int] = {}

    for count_map in count_maps:
        normalized = normalize_appliance_counts(count_map)

        for code, count in normalized.items():
            merged[code] = merged.get(code, 0) + count

    return merged


def apply_machine_exclusivity(
    counts: Mapping[str, int],
    *,
    exclusive_codes: Iterable[str],
) -> dict[str, int]:
    """
    Apply the domestic water washing-machine exclusivity rule.

    Example:
        LL + LV declared together are counted as one effective appliance.

    Declared values are not mutated. The returned mapping is the effective count
    mapping used by the DTU demand calculation.
    """

    normalized_counts = normalize_appliance_counts(counts)
    normalized_exclusive_codes = {
        str(code or "").strip().upper()
        for code in exclusive_codes
        if str(code or "").strip()
    }

    if not normalized_exclusive_codes:
        return normalized_counts

    declared_machine_count = sum(
        count
        for code, count in normalized_counts.items()
        if code.strip().upper() in normalized_exclusive_codes
    )

    if declared_machine_count <= 1:
        return normalized_counts

    first_machine_code = next(
        (
            code
            for code in normalized_counts
            if code.strip().upper() in normalized_exclusive_codes
        ),
        None,
    )

    if first_machine_code is None:
        return normalized_counts

    effective = {
        code: count
        for code, count in normalized_counts.items()
        if code.strip().upper() not in normalized_exclusive_codes
    }
    effective[first_machine_code] = 1

    return effective