from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ndc_core.catalogs.loaders.catalog_paths import singular_losses_cold_water_path
from ndc_core.catalogs.loaders.yaml_loader import load_yaml_file
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.domain.singular_losses import SingularLoss, SingularLossMethod


@dataclass(slots=True)
class SingularLossCatalog:
    """Catalog of singular losses indexed by loss code."""

    losses_by_code: dict[str, SingularLoss] = field(default_factory=dict)
    mappings_by_keyword: dict[str, str] = field(default_factory=dict)
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @staticmethod
    def normalize_key(value: object) -> str:
        text = str(value or "").strip().lower()
        text = text.replace("-", "_").replace(" ", "_")
        while "__" in text:
            text = text.replace("__", "_")
        return text

    def get(self, code: str) -> SingularLoss | None:
        normalized = self.normalize_key(code)

        direct_code = self.mappings_by_keyword.get(normalized, normalized)
        direct = self.losses_by_code.get(direct_code)
        if direct is not None:
            return direct

        for raw_code, loss in self.losses_by_code.items():
            if self.normalize_key(raw_code) == normalized:
                return loss

        return None

    def resolve_loss_code(self, keyword_or_code: str) -> str | None:
        normalized = self.normalize_key(keyword_or_code)
        if not normalized:
            return None

        if normalized in self.mappings_by_keyword:
            return self.mappings_by_keyword[normalized]

        if normalized in self.losses_by_code:
            return normalized

        for raw_code in self.losses_by_code:
            if self.normalize_key(raw_code) == normalized:
                return raw_code

        return None

    def list_codes(self) -> list[str]:
        return sorted(self.losses_by_code)

    @classmethod
    def from_yaml_file(cls, path: Path | None = None) -> Result[SingularLossCatalog]:
        yaml_result = load_yaml_file(path or singular_losses_cold_water_path())
        if yaml_result.failed or yaml_result.value is None:
            return Result.failure(messages=yaml_result.messages)

        return cls.from_mapping(
            yaml_result.value,
            source=str(path or singular_losses_cold_water_path()),
        )

    @classmethod
    def from_mapping(
        cls,
        data: dict[str, Any],
        *,
        source: str = "singular_losses",
    ) -> Result[SingularLossCatalog]:
        messages: list[EngineMessage] = []
        losses: dict[str, SingularLoss] = {}

        _load_k_catalog(data, source=source, losses=losses, messages=messages)
        _load_kv_catalog(data, source=source, losses=losses, messages=messages)

        mappings = _load_mappings(data)

        catalog = cls(
            losses_by_code=losses,
            mappings_by_keyword=mappings,
            messages=tuple(messages),
        )

        return Result.success(value=catalog, messages=messages)


def _load_k_catalog(
    data: dict[str, Any],
    *,
    source: str,
    losses: dict[str, SingularLoss],
    messages: list[EngineMessage],
) -> None:
    raw_catalog = data.get("k_catalog", {})
    if not isinstance(raw_catalog, dict):
        messages.append(
            EngineMessage.warning(
                code="SINGULAR_K_CATALOG_INVALID",
                text="k_catalog must be a mapping.",
                context={"source": source},
            )
        )
        return

    for group_key, raw_group in raw_catalog.items():
        if not isinstance(raw_group, dict):
            continue

        raw_items = raw_group.get("items", [])
        if not isinstance(raw_items, list):
            messages.append(
                EngineMessage.warning(
                    code="SINGULAR_K_ITEMS_INVALID",
                    text="k_catalog group items must be a list.",
                    context={"source": source, "group_key": group_key},
                )
            )
            continue

        for raw_item in raw_items:
            if not isinstance(raw_item, dict):
                continue

            code = str(raw_item.get("id") or "").strip()
            if not code:
                continue

            losses[code] = SingularLoss(
                code=code,
                name=str(raw_item.get("label") or code),
                method=SingularLossMethod.ZETA,
                zeta=_to_optional_float(raw_item.get("k")),
                quantity=1,
                metadata={
                    "group_key": group_key,
                    "family": raw_group.get("family"),
                    "model": raw_item.get("model", "constant"),
                    "angle_deg": raw_item.get("angle_deg"),
                    "flow_path": raw_item.get("flow_path"),
                    "k_table": raw_item.get("k_table"),
                    "formula": raw_item.get("formula"),
                    "source": raw_item.get("source"),
                    "note": raw_item.get("note"),
                },
            )


def _load_kv_catalog(
    data: dict[str, Any],
    *,
    source: str,
    losses: dict[str, SingularLoss],
    messages: list[EngineMessage],
) -> None:
    raw_catalog = data.get("kv_catalog", {})
    if not isinstance(raw_catalog, dict):
        messages.append(
            EngineMessage.warning(
                code="SINGULAR_KV_CATALOG_INVALID",
                text="kv_catalog must be a mapping.",
                context={"source": source},
            )
        )
        return

    for group_key, raw_group in raw_catalog.items():
        if not isinstance(raw_group, dict):
            continue

        raw_items = raw_group.get("items", [])
        if not isinstance(raw_items, list):
            messages.append(
                EngineMessage.warning(
                    code="SINGULAR_KV_ITEMS_INVALID",
                    text="kv_catalog group items must be a list.",
                    context={"source": source, "group_key": group_key},
                )
            )
            continue

        for raw_item in raw_items:
            if not isinstance(raw_item, dict):
                continue

            code = str(raw_item.get("id") or "").strip()
            if not code:
                continue

            dn_kv = raw_item.get("dn_kv")
            representative_kv = None
            if isinstance(dn_kv, dict) and dn_kv:
                representative_kv = max(_to_float(value) for value in dn_kv.values())

            losses[code] = SingularLoss(
                code=code,
                name=str(raw_item.get("label") or code),
                method=SingularLossMethod.KV,
                kv=representative_kv,
                quantity=1,
                metadata={
                    "group_key": group_key,
                    "family": raw_group.get("family"),
                    "manufacturer": raw_group.get("manufacturer"),
                    "reference": raw_group.get("reference"),
                    "position": raw_item.get("position"),
                    "dn_kv": dn_kv,
                    "note": raw_item.get("note"),
                    "comment": raw_item.get("comment"),
                },
            )


def _load_mappings(data: dict[str, Any]) -> dict[str, str]:
    raw_mappings = data.get("mappings", {})
    if isinstance(raw_mappings, dict):
        by_keywords = raw_mappings.get("by_keywords", {})
        if isinstance(by_keywords, dict):
            return {
                SingularLossCatalog.normalize_key(key): str(value).strip()
                for key, value in by_keywords.items()
                if SingularLossCatalog.normalize_key(key) and str(value).strip()
            }

    return {}


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