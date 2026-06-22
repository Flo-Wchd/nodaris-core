from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import DiameterMode, SectionUsageContext
from ndc_core.domain.singular_losses import SingularLoss


def test_section_normalizes_identity_and_geometry() -> None:
    section = Section(
        id=" S1 ",
        name=" Tronçon 1 ",
        upstream_node_id=" N1 ",
        downstream_node_id=" N2 ",
        fluid_code=" EFS ",
        usage_context=SectionUsageContext.RISER,
        length_m=-10.0,
    )

    assert section.id == "S1"
    assert section.name == "Tronçon 1"
    assert section.upstream_node_id == "N1"
    assert section.downstream_node_id == "N2"
    assert section.fluid_code == "EFS"
    assert section.length_m == 0.0


def test_section_diameter_mode_automatic() -> None:
    section = Section(
        id="S1",
        name="Section",
        upstream_node_id="N1",
        downstream_node_id="N2",
        fluid_code="EFS",
    )

    assert section.diameter_mode is DiameterMode.AUTOMATIC
    assert not section.has_forced_diameter


def test_section_diameter_mode_forced_pipe() -> None:
    section = Section(
        id="S1",
        name="Section",
        upstream_node_id="N1",
        downstream_node_id="N2",
        fluid_code="EFS",
        forced_pipe_size_code="cu_12x1",
    )

    assert section.diameter_mode is DiameterMode.FORCED_PIPE
    assert section.has_forced_diameter


def test_section_diameter_mode_forced_internal_diameter() -> None:
    section = Section(
        id="S1",
        name="Section",
        upstream_node_id="N1",
        downstream_node_id="N2",
        fluid_code="EFS",
        forced_internal_diameter_mm=12.0,
    )

    assert section.diameter_mode is DiameterMode.FORCED_INTERNAL_DIAMETER
    assert section.used_internal_diameter_mm == 12.0


def test_section_total_pressure_loss() -> None:
    section = Section(
        id="S1",
        name="Section",
        upstream_node_id="N1",
        downstream_node_id="N2",
        fluid_code="EFS",
    )

    assert section.total_pressure_loss_pa is None

    section.linear_pressure_loss_pa = 100.0
    section.singular_pressure_loss_pa = 20.0
    section.elevation_pressure_loss_pa = 50.0

    assert section.total_pressure_loss_pa == 170.0


def test_section_appliance_counts() -> None:
    section = Section(
        id="S1",
        name="Section",
        upstream_node_id="N1",
        downstream_node_id="N2",
        fluid_code="EFS",
    )

    section.set_downstream_appliance_count("lavabo", 2)
    section.set_effective_appliance_count("lavabo", 1)

    assert section.downstream_appliance_counts == {"lavabo": 2}
    assert section.effective_appliance_counts == {"lavabo": 1}


def test_section_add_singular_loss_only_when_active() -> None:
    section = Section(
        id="S1",
        name="Section",
        upstream_node_id="N1",
        downstream_node_id="N2",
        fluid_code="EFS",
    )

    section.add_singular_loss(SingularLoss(code="elbow", name="Elbow", quantity=1))
    section.add_singular_loss(SingularLoss(code="inactive", name="Inactive", quantity=0))

    assert len(section.singular_losses) == 1


def test_section_clear_calculation_state_preserves_inputs() -> None:
    section = Section(
        id="S1",
        name="Section",
        upstream_node_id="N1",
        downstream_node_id="N2",
        fluid_code="EFS",
        forced_internal_diameter_mm=12.0,
    )
    section.selected_internal_diameter_mm = 14.0
    section.flow_l_s = 0.2
    section.velocity_m_s = 1.0
    section.linear_pressure_loss_pa = 100.0
    section.set_downstream_appliance_count("lavabo", 1)

    section.clear_calculation_state()

    assert section.forced_internal_diameter_mm == 12.0
    assert section.selected_internal_diameter_mm is None
    assert section.flow_l_s is None
    assert section.velocity_m_s is None
    assert section.linear_pressure_loss_pa is None
    assert section.downstream_appliance_counts == {}