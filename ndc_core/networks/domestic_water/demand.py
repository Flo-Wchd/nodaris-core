from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
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
from ndc_core.networks.domestic_water.appliance_counts import (
    apply_machine_exclusivity,
    normalize_appliance_counts,
)
from ndc_core.networks.domestic_water.appliance_rules import (
    appliance_flow_for_profile,
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

        declared_counts = normalize_appliance_counts(appliance_counts)
        effective_counts = apply_machine_exclusivity(
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

            unit_flow_l_s = appliance_flow_for_profile(appliance, self.profile)
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