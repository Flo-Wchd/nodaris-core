from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ndc_core.catalogs.loaders.catalog_paths import appliances_path
from ndc_core.catalogs.loaders.yaml_loader import load_yaml_file
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.domain.appliances import Appliance


@dataclass(slots=True)
class ApplianceCatalog:
    """Catalog of sanitary appliances indexed by appliance code."""

    appliances_by_code: dict[str, Appliance] = field(default_factory=dict)
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @staticmethod
    def normalize_code(value: object) -> str:
        return str(value or "").strip()

    def get(self, code: str) -> Appliance | None:
        normalized = self.normalize_code(code)
        if not normalized:
            return None

        direct = self.appliances_by_code.get(normalized)
        if direct is not None:
            return direct

        lowered = normalized.lower()
        for raw_code, appliance in self.appliances_by_code.items():
            if raw_code.lower() == lowered:
                return appliance

        return None

    def list_codes(self) -> list[str]:
        return sorted(self.appliances_by_code)

    def list_appliances(self) -> list[Appliance]:
        return [self.appliances_by_code[code] for code in self.list_codes()]

    @classmethod
    def from_yaml_file(cls, path: Path | None = None) -> Result[ApplianceCatalog]:
        yaml_result = load_yaml_file(path or appliances_path())
        if yaml_result.failed or yaml_result.value is None:
            return Result.failure(messages=yaml_result.messages)

        return cls.from_mapping(yaml_result.value, source=str(path or appliances_path()))

    @classmethod
    def from_mapping(
        cls,
        data: dict[str, Any],
        *,
        source: str = "appliances",
    ) -> Result[ApplianceCatalog]:
        messages: list[EngineMessage] = []
        appliances: dict[str, Appliance] = {}

        ignored_keys = {"metadata", "units", "fluids"}

        for raw_code, raw_item in data.items():
            if raw_code in ignored_keys:
                continue

            if not isinstance(raw_item, dict):
                messages.append(
                    EngineMessage.warning(
                        code="APPLIANCE_ENTRY_INVALID",
                        text="Appliance entry must be a mapping.",
                        context={"source": source, "appliance_code": raw_code},
                    )
                )
                continue

            appliance_code = cls.normalize_code(raw_item.get("acronym") or raw_code)
            if not appliance_code:
                messages.append(
                    EngineMessage.warning(
                        code="APPLIANCE_CODE_EMPTY",
                        text="Appliance code is empty.",
                        context={"source": source, "raw_code": raw_code},
                    )
                )
                continue

            appliance = Appliance(
                code=appliance_code,
                name=str(raw_item.get("name") or appliance_code),
                cold_water_flow_l_s=_to_float(raw_item.get("cold_design_flow_lps")),
                hot_water_flow_l_s=_to_float(raw_item.get("hot_design_flow_lps")),
                min_internal_diameter_mm=_first_number(
                    raw_item.get("cold_min_diameter_mm"),
                    raw_item.get("hot_min_diameter_mm"),
                ),
                individual_coefficient=_to_optional_float(
                    raw_item.get("individual_coefficient")
                ),
                load_units=_to_optional_float(raw_item.get("load_units")),
            )

            appliances[appliance.code] = appliance

        catalog = cls(
            appliances_by_code=appliances,
            messages=tuple(messages),
        )

        return Result.success(value=catalog, messages=messages)


def _to_float(value: object, default: float = 0.0) -> float:
    if value is None:
        return default

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_optional_float(value: object) -> float | None:
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _first_number(*values: object) -> float | None:
    for value in values:
        number = _to_optional_float(value)
        if number is not None:
            return number

    return None