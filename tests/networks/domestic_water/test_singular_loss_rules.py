from __future__ import annotations

from dataclasses import dataclass
from math import isclose

from ndc_core.catalogs.singular_loss_catalog import SingularLossCatalog
from ndc_core.common.messages import EngineMessage
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import SectionUsageContext
from ndc_core.domain.singular_losses import SingularLoss, SingularLossMethod
from ndc_core.networks.domestic_water.singular_loss_rules import (
    collect_section_singular_zeta_values,
    zeta_from_section_singular_loss_item,
)


@dataclass
class _DirectZeta:
    zeta: float
    quantity: float = 1.0


@dataclass
class _CatalogLoss:
    loss_code: str
    quantity: float = 1.0


def _section() -> Section:
    return Section(
        id="S1",
        name="Section 1",
        upstream_node_id="N1",
        downstream_node_id="N2",
        fluid_code="EFS",
        usage_context=SectionUsageContext.RISER,
        length_m=10.0,
    )


def _catalog() -> SingularLossCatalog:
    return SingularLossCatalog(
        losses_by_code={
            "elbow_90": SingularLoss(
                code="elbow_90",
                name="Elbow 90",
                method=SingularLossMethod.ZETA,
                zeta=0.7,
            ),
            "valve": SingularLoss(
                code="valve",
                name="Valve",
                method=SingularLossMethod.KV,
                kv=3.6,
            ),
        },
        mappings_by_keyword={
            "coude_90": "elbow_90",
            "vanne": "valve",
        },
    )


def test_zeta_from_direct_section_item() -> None:
    messages: list[EngineMessage] = []

    zeta = zeta_from_section_singular_loss_item(
        item=_DirectZeta(zeta=1.2, quantity=2.0),
        section=_section(),
        singular_loss_catalog=None,
        flow_l_s=0.2,
        velocity_m_s=1.0,
        density_kg_m3=1000.0,
        messages=messages,
    )

    assert zeta == 2.4
    assert messages == []


def test_zeta_from_catalog_zeta_loss() -> None:
    messages: list[EngineMessage] = []

    zeta = zeta_from_section_singular_loss_item(
        item=_CatalogLoss(loss_code="coude_90", quantity=2.0),
        section=_section(),
        singular_loss_catalog=_catalog(),
        flow_l_s=0.2,
        velocity_m_s=1.0,
        density_kg_m3=1000.0,
        messages=messages,
    )

    assert isclose(zeta, 1.4)
    assert messages == []


def test_zeta_from_catalog_kv_loss() -> None:
    messages: list[EngineMessage] = []

    zeta = zeta_from_section_singular_loss_item(
        item=_CatalogLoss(loss_code="vanne"),
        section=_section(),
        singular_loss_catalog=_catalog(),
        flow_l_s=0.2,
        velocity_m_s=1.0,
        density_kg_m3=1000.0,
        messages=messages,
    )

    assert zeta > 0.0
    assert messages == []


def test_unknown_catalog_loss_adds_warning() -> None:
    messages: list[EngineMessage] = []

    zeta = zeta_from_section_singular_loss_item(
        item=_CatalogLoss(loss_code="unknown"),
        section=_section(),
        singular_loss_catalog=_catalog(),
        flow_l_s=0.2,
        velocity_m_s=1.0,
        density_kg_m3=1000.0,
        messages=messages,
    )

    assert zeta == 0.0
    assert len(messages) == 1
    assert messages[0].code == "DOMESTIC_WATER_SINGULAR_LOSS_UNKNOWN"


def test_missing_catalog_adds_warning() -> None:
    messages: list[EngineMessage] = []

    zeta = zeta_from_section_singular_loss_item(
        item=_CatalogLoss(loss_code="coude_90"),
        section=_section(),
        singular_loss_catalog=None,
        flow_l_s=0.2,
        velocity_m_s=1.0,
        density_kg_m3=1000.0,
        messages=messages,
    )

    assert zeta == 0.0
    assert len(messages) == 1
    assert messages[0].code == "DOMESTIC_WATER_SINGULAR_CATALOG_MISSING"


def test_kv_loss_without_flow_adds_warning() -> None:
    messages: list[EngineMessage] = []

    zeta = zeta_from_section_singular_loss_item(
        item=_CatalogLoss(loss_code="vanne"),
        section=_section(),
        singular_loss_catalog=_catalog(),
        flow_l_s=0.0,
        velocity_m_s=0.0,
        density_kg_m3=1000.0,
        messages=messages,
    )

    assert zeta == 0.0
    assert len(messages) == 1
    assert messages[0].code == "DOMESTIC_WATER_KV_SKIPPED_NO_FLOW"


def test_collect_section_singular_zeta_values() -> None:
    section = _section()
    section.singular_losses.append(_DirectZeta(zeta=1.0, quantity=2.0))
    section.singular_losses.append(_CatalogLoss(loss_code="coude_90", quantity=2.0))

    messages: list[EngineMessage] = []

    values = collect_section_singular_zeta_values(
        section=section,
        singular_loss_catalog=_catalog(),
        flow_l_s=0.2,
        velocity_m_s=1.0,
        density_kg_m3=1000.0,
        messages=messages,
    )

    assert values == (2.0, 1.4)
    assert messages == []