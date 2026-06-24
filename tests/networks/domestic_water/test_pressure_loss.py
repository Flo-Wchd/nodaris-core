from math import isclose

from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.catalogs.singular_loss_catalog import SingularLossCatalog
from ndc_core.domain.fluids import Fluid
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import SectionUsageContext
from ndc_core.domain.pipes import PipeMaterial, PipeSize
from ndc_core.domain.singular_losses import SingularLoss, SingularLossMethod
from ndc_core.networks.domestic_water.pressure_loss import (
    compute_cold_water_section_pressure_loss,
    compute_hot_water_section_pressure_loss,
)
from ndc_core.networks.domestic_water.pressure_loss_types import (
    DomesticWaterPressureLossMode,
)


class _DirectZeta:
    def __init__(self, zeta: float, quantity: float = 1.0) -> None:
        self.zeta = zeta
        self.quantity = quantity


class _CatalogLoss:
    def __init__(self, loss_code: str, quantity: float = 1.0) -> None:
        self.loss_code = loss_code
        self.quantity = quantity


def _fluid_catalog() -> FluidCatalog:
    cold = Fluid(
        code="cold_water",
        name="Cold water",
        temperature_c=10.0,
        density_kg_m3=1000.0,
        dynamic_viscosity_pa_s=0.001,
    )
    hot = Fluid(
        code="hot_water",
        name="Hot water",
        temperature_c=60.0,
        density_kg_m3=983.0,
        dynamic_viscosity_pa_s=0.000466,
    )

    return FluidCatalog(
        fluids_by_code={
            cold.code: cold,
            hot.code: hot,
        },
        water_points_by_temperature={
            10.0: cold,
            60.0: hot,
        },
    )


def _pipe_catalog() -> PipeCatalog:
    material = PipeMaterial(
        code="EFS",
        name="Test material",
        default_roughness_m=0.0000015,
    )
    size = PipeSize(
        code="P20",
        material_code="EFS",
        nominal_diameter="DN20",
        internal_diameter_mm=20.0,
    )

    return PipeCatalog(
        materials_by_code={"EFS": material},
        sizes_by_code={"P20": size},
        size_codes_by_material={"EFS": ["P20"]},
    )


def _singular_loss_catalog() -> SingularLossCatalog:
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


def _section(**kwargs: object) -> Section:
    values = {
        "id": "S1",
        "name": "Section 1",
        "upstream_node_id": "N1",
        "downstream_node_id": "N2",
        "fluid_code": "EFS",
        "usage_context": SectionUsageContext.RISER,
        "length_m": 10.0,
        "elevation_change_m": 1.0,
    }
    values.update(kwargs)

    section = Section(**values)
    section.flow_l_s = 0.2
    section.selected_pipe_size_code = "P20"
    section.selected_internal_diameter_mm = 20.0

    return section


def test_compute_cold_water_section_pressure_loss_with_direct_zeta() -> None:
    section = _section()
    section.singular_losses.append(_DirectZeta(zeta=1.0, quantity=2.0))

    result = compute_cold_water_section_pressure_loss(
        section=section,
        fluid_catalog=_fluid_catalog(),
        pipe_catalog=_pipe_catalog(),
    )

    assert result.ok
    assert result.value is not None

    pressure = result.value

    assert pressure.mode is DomesticWaterPressureLossMode.FULL
    assert pressure.flow_l_s == 0.2
    assert pressure.internal_diameter_mm == 20.0
    assert pressure.velocity_m_s > 0.0
    assert pressure.reynolds is not None
    assert pressure.linear_pressure_loss_pa > 0.0
    assert pressure.singular_pressure_loss_pa > 0.0
    assert pressure.elevation_pressure_change_pa == 9810.0
    assert pressure.total_pressure_change_pa > 9810.0

    assert section.velocity_m_s == pressure.velocity_m_s
    assert section.reynolds == pressure.reynolds
    assert section.linear_pressure_loss_pa == pressure.linear_pressure_loss_pa
    assert section.singular_pressure_loss_pa == pressure.singular_pressure_loss_pa
    assert section.elevation_pressure_loss_pa == pressure.elevation_pressure_change_pa
    assert section.total_pressure_loss_pa == pressure.total_pressure_change_pa
    assert section.singular_zeta_total == 2.0


def test_compute_pressure_loss_uses_pipe_catalog_roughness() -> None:
    section = _section()

    result = compute_cold_water_section_pressure_loss(
        section=section,
        fluid_catalog=_fluid_catalog(),
        pipe_catalog=_pipe_catalog(),
    )

    assert result.ok
    assert result.value is not None
    assert result.value.relative_roughness_value > 0.0


def test_compute_pressure_loss_from_catalog_zeta() -> None:
    section = _section()
    section.singular_losses.append(_CatalogLoss("coude_90", quantity=2.0))

    result = compute_cold_water_section_pressure_loss(
        section=section,
        fluid_catalog=_fluid_catalog(),
        pipe_catalog=_pipe_catalog(),
        singular_loss_catalog=_singular_loss_catalog(),
    )

    assert result.ok
    assert result.value is not None
    assert isclose(result.value.breakdown.singular_zeta_total, 1.4)


def test_compute_pressure_loss_from_catalog_kv() -> None:
    section = _section()
    section.singular_losses.append(_CatalogLoss("vanne"))

    result = compute_cold_water_section_pressure_loss(
        section=section,
        fluid_catalog=_fluid_catalog(),
        pipe_catalog=_pipe_catalog(),
        singular_loss_catalog=_singular_loss_catalog(),
    )

    assert result.ok
    assert result.value is not None
    assert result.value.breakdown.singular_zeta_total > 0.0
    assert result.value.singular_pressure_loss_pa > 0.0


def test_missing_diameter_returns_failure_without_exception() -> None:
    section = _section()
    section.selected_internal_diameter_mm = None

    result = compute_cold_water_section_pressure_loss(
        section=section,
        fluid_catalog=_fluid_catalog(),
        pipe_catalog=_pipe_catalog(),
    )

    assert result.failed
    assert result.value is None
    assert any(
        message.code == "DOMESTIC_WATER_PRESSURE_DIAMETER_MISSING"
        for message in result.messages
    )


def test_zero_flow_keeps_elevation_only() -> None:
    section = _section(elevation_change_m=-2.0)
    section.flow_l_s = 0.0

    result = compute_cold_water_section_pressure_loss(
        section=section,
        fluid_catalog=_fluid_catalog(),
        pipe_catalog=_pipe_catalog(),
    )

    assert result.ok
    assert result.value is not None

    pressure = result.value

    assert pressure.mode is DomesticWaterPressureLossMode.ELEVATION_ONLY
    assert pressure.linear_pressure_loss_pa == 0.0
    assert pressure.singular_pressure_loss_pa == 0.0
    assert pressure.elevation_pressure_change_pa == -19_620.0
    assert pressure.total_pressure_change_pa == -19_620.0


def test_hot_water_uses_hot_water_fluid_by_default() -> None:
    section = _section(fluid_code="ECS")

    result = compute_hot_water_section_pressure_loss(
        section=section,
        fluid_catalog=_fluid_catalog(),
        pipe_catalog=_pipe_catalog(),
    )

    assert result.ok
    assert result.value is not None
    assert result.value.fluid.code == "hot_water"
    assert result.value.fluid.temperature_c == 60.0


def test_temperature_override_uses_interpolated_water() -> None:
    section = _section()

    result = compute_cold_water_section_pressure_loss(
        section=section,
        fluid_catalog=_fluid_catalog(),
        pipe_catalog=_pipe_catalog(),
        water_temperature_c=10.0,
    )

    assert result.ok
    assert result.value is not None
    assert result.value.fluid.temperature_c == 10.0


def test_unknown_singular_loss_creates_warning_without_failure() -> None:
    section = _section()
    section.singular_losses.append(_CatalogLoss("unknown_loss"))

    result = compute_cold_water_section_pressure_loss(
        section=section,
        fluid_catalog=_fluid_catalog(),
        pipe_catalog=_pipe_catalog(),
        singular_loss_catalog=_singular_loss_catalog(),
    )

    assert result.ok
    assert result.value is not None
    assert result.value.has_warnings
    assert any(
        message.code == "DOMESTIC_WATER_SINGULAR_LOSS_UNKNOWN"
        for message in result.value.messages
    )