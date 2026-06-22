from ndc_core.domain.pipes import PipeSize
from ndc_core.hydraulics.pipe_sizing import (
    select_pipe_size_by_velocity,
    select_smallest_usable_pipe_size,
)


def test_select_smallest_usable_pipe_size() -> None:
    sizes = [
        PipeSize(
            code="DN10",
            material_code="test",
            nominal_diameter="DN10",
            internal_diameter_mm=10.0,
        ),
        PipeSize(
            code="DN20",
            material_code="test",
            nominal_diameter="DN20",
            internal_diameter_mm=20.0,
        ),
    ]

    selected = select_smallest_usable_pipe_size(
        sizes,
        minimum_internal_diameter_mm=12.0,
    )

    assert selected is not None
    assert selected.code == "DN20"


def test_select_pipe_size_by_velocity() -> None:
    sizes = [
        PipeSize(
            code="DN10",
            material_code="test",
            nominal_diameter="DN10",
            internal_diameter_mm=10.0,
        ),
        PipeSize(
            code="DN20",
            material_code="test",
            nominal_diameter="DN20",
            internal_diameter_mm=20.0,
        ),
    ]

    result = select_pipe_size_by_velocity(
        design_flow_l_s=0.2,
        pipe_sizes=sizes,
        max_velocity_m_s=2.0,
    )

    assert result.found
    assert result.selected_pipe_size is not None
    assert result.selected_pipe_size.code in {"DN10", "DN20"}
    assert result.theoretical_internal_diameter_mm is not None
    assert result.real_velocity_m_s is not None
    assert result.velocity_ok is not None


def test_select_pipe_size_by_velocity_returns_largest_if_all_too_small() -> None:
    sizes = [
        PipeSize(
            code="DN10",
            material_code="test",
            nominal_diameter="DN10",
            internal_diameter_mm=10.0,
        ),
    ]

    result = select_pipe_size_by_velocity(
        design_flow_l_s=10.0,
        pipe_sizes=sizes,
        max_velocity_m_s=1.0,
    )

    assert result.selected_pipe_size is not None
    assert result.selected_pipe_size.code == "DN10"
    assert result.velocity_ok is False