from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.domain.appliances import Appliance
from ndc_core.networks.domestic_water.profiles import (
    COLD_WATER_PROFILE,
    HOT_WATER_PROFILE,
    DomesticWaterProfile,
)
from ndc_core.networks.domestic_water.simultaneity import (
    clamp_simultaneity_factor,
    collective_dtu_simultaneity_factor,
)
from ndc_core.networks.domestic_water.types import (
    ApplianceDemandItem,
    DomesticWaterDemand,
    DomesticWaterMethod,
)


@dataclass(frozen=True, slots=True)
class DomesticWaterDemandBuilder:
    """Build theoretical EFS/ECS forward demand from appliance counts."""

    appliance_catalog: ApplianceCatalog
    profile: DomesticWaterProfile

    @classmethod
    def cold_water(cls, appliance_catalog: ApplianceCatalog) -> DomesticWaterDemandBuilder:
        return cls(appliance_catalog=appliance_catalog, profile=COLD_WATER_PROFILE)

    @classmethod
    def hot_water(cls, appliance_catalog: ApplianceCatalog) -> DomesticWaterDemandBuilder:
        return cls(appliance_catalog=appliance_catalog, profile=HOT_WATER_PROFILE)

    def compute_from_counts(
        self,
        appliance_counts: Mapping[str, int],
    ) -> Result[DomesticWaterDemand]:
        messages: list[EngineMessage] = []

        declared_counts = _normalize_counts(appliance_counts)
        effective_counts = _apply_machine_exclusivity(
            declared_counts,
            exclusive_codes=self.profile.machine_exclusive_codes,
        )

        if declared_counts != effective_counts:
            messages.append(
                EngineMessage.info(
                    code="DOMESTIC_WATER_MACHINE_EXCLUSIVITY_APPLIED",
                    text=(
                        "Machine exclusivity rule applied: several washing machines "
                        "are counted as one effective appliance."
                    ),
                    context={
                        "declared_counts": declared_counts,
                        "effective_counts": effective_counts,
                    },
                )
            )

        items: list[ApplianceDemandItem] = []
        declared_appliance_count = sum(declared_counts.values())
        effective_appliance_count = sum(effective_counts.values())
        raw_flow_l_s = 0.0

        for appliance_code in sorted(effective_counts):
            effective_count = effective_counts[appliance_code]
            declared_count = declared_counts.get(appliance_code, effective_count)
            appliance = self.appliance_catalog.get(appliance_code)

            if appliance is None:
                messages.append(
                    EngineMessage.warning(
                        code="DOMESTIC_WATER_UNKNOWN_APPLIANCE",
                        text="Appliance is not defined in the catalog.",
                        context={"appliance_code": appliance_code},
                    )
                )
                continue

            unit_flow_l_s = _flow_for_profile(appliance, self.profile)
            if unit_flow_l_s <= 0.0:
                messages.append(
                    EngineMessage.info(
                        code="DOMESTIC_WATER_APPLIANCE_IGNORED_FOR_SIDE",
                        text="Appliance has no design flow for this domestic water side.",
                        context={
                            "appliance_code": appliance_code,
                            "side": self.profile.side.value,
                        },
                    )
                )
                continue

            total_flow_l_s = unit_flow_l_s * effective_count
            raw_flow_l_s += total_flow_l_s

            items.append(
                ApplianceDemandItem(
                    appliance_code=appliance.code,
                    appliance_name=appliance.name,
                    declared_count=declared_count,
                    effective_count=effective_count,
                    unit_flow_l_s=unit_flow_l_s,
                    total_flow_l_s=total_flow_l_s,
                )
            )

        simultaneity_factor = self._simultaneity_factor(effective_appliance_count)
        design_flow_l_s = raw_flow_l_s * simultaneity_factor

        demand = DomesticWaterDemand(
            side=self.profile.side,
            method=self.profile.method,
            declared_appliance_count=declared_appliance_count,
            effective_appliance_count=effective_appliance_count,
            raw_flow_l_s=raw_flow_l_s,
            simultaneity_factor=simultaneity_factor,
            design_flow_l_s=design_flow_l_s,
            items=tuple(items),
            messages=tuple(messages),
        )

        return Result.success(value=demand, messages=messages)

    def _simultaneity_factor(self, effective_appliance_count: int) -> float:
        if self.profile.method is DomesticWaterMethod.RAW_SUM:
            return 1.0

        return clamp_simultaneity_factor(
            collective_dtu_simultaneity_factor(
                effective_appliance_count,
                threshold=self.profile.simultaneity_threshold,
            )
        )


def compute_cold_water_demand(
    appliance_catalog: ApplianceCatalog,
    appliance_counts: Mapping[str, int],
) -> Result[DomesticWaterDemand]:
    """Convenience function for EFS demand."""

    return DomesticWaterDemandBuilder.cold_water(appliance_catalog).compute_from_counts(
        appliance_counts
    )


def compute_hot_water_demand(
    appliance_catalog: ApplianceCatalog,
    appliance_counts: Mapping[str, int],
) -> Result[DomesticWaterDemand]:
    """Convenience function for ECS forward demand."""

    return DomesticWaterDemandBuilder.hot_water(appliance_catalog).compute_from_counts(
        appliance_counts
    )


def _normalize_counts(appliance_counts: Mapping[str, int]) -> dict[str, int]:
    normalized: dict[str, int] = {}

    for raw_code, raw_count in appliance_counts.items():
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


def _apply_machine_exclusivity(
    counts: Mapping[str, int],
    *,
    exclusive_codes: frozenset[str],
) -> dict[str, int]:
    """
    Apply LL + LV counted as one effective machine.

    Declared values are preserved outside this function. The demand result keeps
    both declared_count and effective_count for GUI/export transparency.
    """

    effective = dict(counts)

    declared_machine_count = sum(
        count
        for code, count in counts.items()
        if code.strip().upper() in exclusive_codes
    )

    if declared_machine_count <= 1:
        return effective

    first_machine_code = next(
        (
            code
            for code in counts
            if code.strip().upper() in exclusive_codes
        ),
        None,
    )

    if first_machine_code is None:
        return effective

    for code in list(effective):
        if code.strip().upper() in exclusive_codes:
            effective.pop(code)

    effective[first_machine_code] = 1
    return effective


def _flow_for_profile(
    appliance: Appliance,
    profile: DomesticWaterProfile,
) -> float:
    value = getattr(appliance, profile.flow_attribute_name, 0.0)

    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return 0.0