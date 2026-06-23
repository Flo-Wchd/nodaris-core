from __future__ import annotations

from typing import Any

from ndc_core.catalogs.singular_loss_catalog import SingularLossCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.domain.networks.section import Section
from ndc_core.domain.singular_losses import SingularLoss, SingularLossMethod
from ndc_core.hydraulics.singular_pressure_loss import equivalent_zeta_from_kv
from ndc_core.networks.domestic_water.entity_access import clean_optional_code
from ndc_core.networks.domestic_water.numeric import safe_positive_float


def collect_section_singular_zeta_values(
    *,
    section: Section,
    singular_loss_catalog: SingularLossCatalog | None,
    flow_l_s: float,
    velocity_m_s: float,
    density_kg_m3: float,
    messages: list[EngineMessage],
) -> tuple[float, ...]:
    """
    Collect positive singular zeta values declared on a section.

    Supports:
    - direct zeta items declared on the section;
    - zeta-based catalog losses;
    - Kv-based catalog losses converted to equivalent zeta.

    Invalid, missing or unsupported items are ignored with managed warnings.
    """

    zeta_values: list[float] = []

    for item in section.singular_losses:
        zeta = zeta_from_section_singular_loss_item(
            item=item,
            section=section,
            singular_loss_catalog=singular_loss_catalog,
            flow_l_s=flow_l_s,
            velocity_m_s=velocity_m_s,
            density_kg_m3=density_kg_m3,
            messages=messages,
        )
        if zeta > 0.0:
            zeta_values.append(zeta)

    return tuple(zeta_values)


def zeta_from_section_singular_loss_item(
    *,
    item: Any,
    section: Section,
    singular_loss_catalog: SingularLossCatalog | None,
    flow_l_s: float,
    velocity_m_s: float,
    density_kg_m3: float,
    messages: list[EngineMessage],
) -> float:
    """Resolve one section singular-loss item to an equivalent zeta value."""

    quantity = safe_positive_float(getattr(item, "quantity", 1.0)) or 1.0

    direct_zeta = safe_positive_float(getattr(item, "zeta", None))
    if direct_zeta is not None:
        return direct_zeta * quantity

    loss_code = clean_optional_code(
        getattr(item, "loss_code", None)
        or getattr(item, "singular_loss_code", None)
        or getattr(item, "code", None)
    )
    if loss_code is None:
        return 0.0

    if singular_loss_catalog is None:
        messages.append(
            EngineMessage.warning(
                code="DOMESTIC_WATER_SINGULAR_CATALOG_MISSING",
                text="Singular loss catalog is missing; section singular loss was ignored.",
                context={
                    "section_id": section.id,
                    "loss_code": loss_code,
                },
            )
        )
        return 0.0

    loss = singular_loss_catalog.get(loss_code)
    if loss is None:
        messages.append(
            EngineMessage.warning(
                code="DOMESTIC_WATER_SINGULAR_LOSS_UNKNOWN",
                text="Singular loss code is unknown; section singular loss was ignored.",
                context={
                    "section_id": section.id,
                    "loss_code": loss_code,
                },
            )
        )
        return 0.0

    return zeta_from_catalog_singular_loss(
        loss=loss,
        quantity=quantity,
        section=section,
        flow_l_s=flow_l_s,
        velocity_m_s=velocity_m_s,
        density_kg_m3=density_kg_m3,
        messages=messages,
    )


def zeta_from_catalog_singular_loss(
    *,
    loss: SingularLoss,
    quantity: float,
    section: Section,
    flow_l_s: float,
    velocity_m_s: float,
    density_kg_m3: float,
    messages: list[EngineMessage],
) -> float:
    """Resolve one catalog singular loss to an equivalent zeta value."""

    if loss.method is SingularLossMethod.ZETA:
        return max(0.0, float(loss.zeta or 0.0)) * quantity

    if loss.method is SingularLossMethod.KV:
        if flow_l_s <= 0.0 or velocity_m_s <= 0.0:
            messages.append(
                EngineMessage.warning(
                    code="DOMESTIC_WATER_KV_SKIPPED_NO_FLOW",
                    text="Kv singular loss was ignored because flow or velocity is missing.",
                    context={
                        "section_id": section.id,
                        "loss_code": loss.code,
                    },
                )
            )
            return 0.0

        zeta = equivalent_zeta_from_kv(
            flow_l_s=flow_l_s,
            kv_m3_h=float(loss.kv or 0.0),
            velocity_m_s=velocity_m_s,
            density_kg_m3=density_kg_m3,
        )
        return zeta * quantity

    messages.append(
        EngineMessage.warning(
            code="DOMESTIC_WATER_SINGULAR_METHOD_UNSUPPORTED",
            text="Singular loss method is not supported yet for section pressure loss.",
            context={
                "section_id": section.id,
                "loss_code": loss.code,
                "method": loss.method.value,
            },
        )
    )
    return 0.0