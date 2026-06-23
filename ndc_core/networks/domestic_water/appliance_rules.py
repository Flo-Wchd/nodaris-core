from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.domain.appliances import Appliance
from ndc_core.networks.domestic_water.profiles import DomesticWaterProfile


def appliance_flow_for_profile(
    appliance: Appliance,
    profile: DomesticWaterProfile,
) -> float:
    """
    Return the appliance unit design flow for the requested domestic water profile.

    Invalid, missing or negative values are treated as zero.
    """

    value = getattr(appliance, profile.flow_attribute_name, 0.0)

    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return 0.0


def minimum_appliance_internal_diameter_mm(
    *,
    appliance_catalog: ApplianceCatalog,
    appliance_counts: Mapping[str, int],
    profile: DomesticWaterProfile,
) -> float:
    """
    Return the maximum appliance minimum internal diameter required by a profile.

    Appliances with no flow on the requested side are ignored.
    Unknown appliances and invalid diameters are ignored.
    """

    minimum = 0.0

    for code, count in appliance_counts.items():
        if count <= 0:
            continue

        appliance = appliance_catalog.get(code)
        if appliance is None:
            continue

        if appliance_flow_for_profile(appliance, profile) <= 0.0:
            continue

        diameter = _optional_positive_float(appliance.min_internal_diameter_mm)
        if diameter is None:
            continue

        if diameter > minimum:
            minimum = diameter

    return minimum


def _optional_positive_float(value: Any) -> float | None:
    if value is None:
        return None

    try:
        number = float(value)
    except (TypeError, ValueError):
        return None

    if number <= 0.0:
        return None

    return number