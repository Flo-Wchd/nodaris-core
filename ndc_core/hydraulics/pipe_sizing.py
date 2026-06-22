from __future__ import annotations

from collections.abc import Iterable

from ndc_core.domain.pipes import PipeSize
from ndc_core.hydraulics.types import PipeSizingResult
from ndc_core.hydraulics.velocity import (
    theoretical_diameter_mm_for_velocity,
    velocity_from_l_s_and_mm,
)


def select_smallest_usable_pipe_size(
    pipe_sizes: Iterable[PipeSize],
    *,
    minimum_internal_diameter_mm: float,
) -> PipeSize | None:
    """Return the smallest pipe size matching a minimum internal diameter."""

    try:
        minimum_diameter = max(0.0, float(minimum_internal_diameter_mm))
    except (TypeError, ValueError):
        minimum_diameter = 0.0

    candidates = sorted(
        (pipe_size for pipe_size in pipe_sizes if pipe_size.is_usable),
        key=lambda pipe_size: pipe_size.internal_diameter_mm,
    )

    for pipe_size in candidates:
        if pipe_size.internal_diameter_mm >= minimum_diameter:
            return pipe_size

    if candidates:
        return candidates[-1]

    return None


def select_pipe_size_by_velocity(
    *,
    design_flow_l_s: float,
    pipe_sizes: Iterable[PipeSize],
    max_velocity_m_s: float,
    min_internal_diameter_mm: float | None = None,
) -> PipeSizingResult:
    """
    Select the smallest pipe size respecting theoretical diameter by velocity.

    If no candidate is large enough, the largest usable size is returned. The
    caller can inspect ``velocity_ok`` to detect that it still exceeds the limit.
    """

    theoretical_diameter = theoretical_diameter_mm_for_velocity(
        flow_l_s=design_flow_l_s,
        target_velocity_m_s=max_velocity_m_s,
    )

    minimum_diameter = theoretical_diameter
    if min_internal_diameter_mm is not None:
        minimum_diameter = max(theoretical_diameter, min_internal_diameter_mm)

    selected = select_smallest_usable_pipe_size(
        pipe_sizes,
        minimum_internal_diameter_mm=minimum_diameter,
    )

    real_velocity = None
    if selected is not None:
        real_velocity = velocity_from_l_s_and_mm(
            flow_l_s=design_flow_l_s,
            internal_diameter_mm=selected.internal_diameter_mm,
        )

    return PipeSizingResult(
        selected_pipe_size=selected,
        theoretical_internal_diameter_mm=theoretical_diameter or None,
        design_flow_l_s=max(0.0, float(design_flow_l_s)),
        max_velocity_m_s=max(0.0, float(max_velocity_m_s)),
        real_velocity_m_s=real_velocity,
    )