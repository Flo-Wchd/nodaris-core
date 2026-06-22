from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ndc_core.catalogs.loaders.catalog_paths import pipes_path
from ndc_core.catalogs.loaders.yaml_loader import load_yaml_file
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.domain.pipes import PipeMaterial, PipeMaterialFamily, PipeSize


@dataclass(slots=True)
class PipeCatalog:
    """Catalog of pipe materials and commercial pipe sizes."""

    materials_by_code: dict[str, PipeMaterial] = field(default_factory=dict)
    sizes_by_code: dict[str, PipeSize] = field(default_factory=dict)
    size_codes_by_material: dict[str, list[str]] = field(default_factory=dict)
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @staticmethod
    def normalize_code(value: object) -> str:
        return str(value or "").strip()

    def get_material(self, code: str) -> PipeMaterial | None:
        return self.materials_by_code.get(self.normalize_code(code))

    def get_size(self, code: str) -> PipeSize | None:
        normalized = self.normalize_code(code)
        if not normalized:
            return None

        direct = self.sizes_by_code.get(normalized)
        if direct is not None:
            return direct

        lowered = normalized.lower()
        for raw_code, pipe_size in self.sizes_by_code.items():
            if raw_code.lower() == lowered:
                return pipe_size

        return None

    def list_material_codes(self) -> list[str]:
        return sorted(self.materials_by_code)

    def list_size_codes(self) -> list[str]:
        return sorted(self.sizes_by_code)

    def list_sizes_for_material(self, material_code: str) -> list[PipeSize]:
        codes = self.size_codes_by_material.get(self.normalize_code(material_code), [])
        return [self.sizes_by_code[code] for code in codes if code in self.sizes_by_code]

    @classmethod
    def from_yaml_file(cls, path: Path | None = None) -> Result[PipeCatalog]:
        yaml_result = load_yaml_file(path or pipes_path())
        if yaml_result.failed or yaml_result.value is None:
            return Result.failure(messages=yaml_result.messages)

        return cls.from_mapping(yaml_result.value, source=str(path or pipes_path()))

    @classmethod
    def from_mapping(
        cls,
        data: dict[str, Any],
        *,
        source: str = "pipes",
    ) -> Result[PipeCatalog]:
        messages: list[EngineMessage] = []
        materials: dict[str, PipeMaterial] = {}
        sizes: dict[str, PipeSize] = {}
        sizes_by_material: dict[str, list[str]] = {}

        raw_families = data.get("pipe_families", [])
        if not isinstance(raw_families, list):
            return Result.failure(
                messages=[
                    EngineMessage.error(
                        code="PIPE_FAMILIES_INVALID",
                        text="pipe_families must be a list.",
                        context={"source": source},
                    )
                ]
            )

        for raw_family in raw_families:
            if not isinstance(raw_family, dict):
                messages.append(
                    EngineMessage.warning(
                        code="PIPE_FAMILY_INVALID",
                        text="Pipe family entry must be a mapping.",
                        context={"source": source},
                    )
                )
                continue

            family_id = cls.normalize_code(raw_family.get("id"))
            material_code = cls.normalize_code(raw_family.get("material") or family_id)
            family_label = str(raw_family.get("label") or material_code).strip()
            design_defaults = _as_dict(raw_family.get("design_defaults"))

            if not material_code:
                messages.append(
                    EngineMessage.warning(
                        code="PIPE_MATERIAL_CODE_EMPTY",
                        text="Pipe material code is empty.",
                        context={"source": source, "family_id": family_id},
                    )
                )
                continue

            if material_code not in materials:
                materials[material_code] = PipeMaterial(
                    code=material_code,
                    name=family_label,
                    family=_material_family_from_code(material_code),
                    default_roughness_m=_roughness_mm_to_m(
                        design_defaults.get("roughness_mm")
                    ),
                )

            raw_variants = raw_family.get("variants", [])
            if not isinstance(raw_variants, list):
                messages.append(
                    EngineMessage.warning(
                        code="PIPE_VARIANTS_INVALID",
                        text="Pipe family variants must be a list.",
                        context={"source": source, "family_id": family_id},
                    )
                )
                continue

            for raw_variant in raw_variants:
                if not isinstance(raw_variant, dict):
                    messages.append(
                        EngineMessage.warning(
                            code="PIPE_VARIANT_INVALID",
                            text="Pipe variant entry must be a mapping.",
                            context={"source": source, "family_id": family_id},
                        )
                    )
                    continue

                size_code = cls.normalize_code(raw_variant.get("id"))
                if not size_code:
                    messages.append(
                        EngineMessage.warning(
                            code="PIPE_SIZE_CODE_EMPTY",
                            text="Pipe size code is empty.",
                            context={"source": source, "family_id": family_id},
                        )
                    )
                    continue

                pipe_size = PipeSize(
                    code=size_code,
                    material_code=material_code,
                    nominal_diameter=str(raw_variant.get("nominal_dn") or size_code),
                    internal_diameter_mm=_to_float(
                        raw_variant.get("inner_diameter_mm")
                    ),
                    external_diameter_mm=_to_optional_float(
                        raw_variant.get("outer_diameter_mm")
                    ),
                    wall_thickness_mm=_to_optional_float(
                        raw_variant.get("thickness_mm")
                    ),
                )

                sizes[pipe_size.code] = pipe_size
                sizes_by_material.setdefault(material_code, []).append(pipe_size.code)

        catalog = cls(
            materials_by_code=materials,
            sizes_by_code=sizes,
            size_codes_by_material=sizes_by_material,
            messages=tuple(messages),
        )

        return Result.success(value=catalog, messages=messages)


def _as_dict(value: object) -> dict[str, Any]:
    if isinstance(value, dict):
        return value

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


def _roughness_mm_to_m(value: object) -> float:
    return max(0.0, _to_float(value) / 1000.0)


def _material_family_from_code(value: str) -> PipeMaterialFamily:
    normalized = value.strip().lower().replace("-", "_")

    if normalized in {"copper", "cuivre", "cu"}:
        return PipeMaterialFamily.COPPER
    if normalized in {"stainless_steel", "inox"}:
        return PipeMaterialFamily.STAINLESS_STEEL
    if normalized in {"galvanized_steel", "galva", "steel"}:
        return PipeMaterialFamily.GALVANIZED_STEEL
    if normalized in {"pex", "per"}:
        return PipeMaterialFamily.PEX
    if normalized == "pb":
        return PipeMaterialFamily.PB
    if normalized in {"pvc_c", "cpvc"}:
        return PipeMaterialFamily.PVC_C
    if normalized in {"ppr", "pp_r"}:
        return PipeMaterialFamily.PPR
    if normalized in {"multilayer", "multicouche"}:
        return PipeMaterialFamily.MULTILAYER
    if normalized in {"cast_iron", "fonte"}:
        return PipeMaterialFamily.CAST_IRON
    if normalized == "pvc":
        return PipeMaterialFamily.PVC

    return PipeMaterialFamily.OTHER