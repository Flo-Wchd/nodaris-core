from __future__ import annotations

from types import SimpleNamespace

from ndc_core.common.messages import EngineMessage
from ndc_core.networks.domestic_water.network_compute_result import (
    DomesticWaterNetworkComputeResult,
    DomesticWaterNetworkStep,
    DomesticWaterSectionComputeResult,
)
from ndc_core.networks.domestic_water.network_engine import (
    DomesticWaterNetworkComputeResult as EngineNetworkComputeResult,
)
from ndc_core.networks.domestic_water.network_engine import (
    DomesticWaterNetworkStep as EngineNetworkStep,
)
from ndc_core.networks.domestic_water.network_engine import (
    DomesticWaterSectionComputeResult as EngineSectionComputeResult,
)
from ndc_core.networks.domestic_water.types import DomesticWaterSide


def test_network_compute_result_exports_are_kept_from_network_engine() -> None:
    assert EngineNetworkComputeResult is DomesticWaterNetworkComputeResult
    assert EngineSectionComputeResult is DomesticWaterSectionComputeResult
    assert EngineNetworkStep is DomesticWaterNetworkStep


def test_domestic_water_network_step_values() -> None:
    assert DomesticWaterNetworkStep.TOPOLOGY_VALIDATION.value == "topology_validation"
    assert DomesticWaterNetworkStep.SIZING.value == "sizing"
    assert DomesticWaterNetworkStep.PRESSURE_LOSS.value == "pressure_loss"
    assert DomesticWaterNetworkStep.PRESSURE_PROPAGATION.value == "pressure_propagation"
    assert DomesticWaterNetworkStep.PRESSURE_SUMMARY.value == "pressure_summary"


def test_section_compute_result_status_helpers() -> None:
    warning = EngineMessage.warning(
        code="TEST_WARNING",
        text="Test warning.",
        context={"section_id": "S1"},
    )

    result = DomesticWaterSectionComputeResult(
        section_id="S1",
        sizing=SimpleNamespace(has_errors=False),
        pressure_loss=SimpleNamespace(has_errors=False),
        messages=(warning,),
    )

    assert result.sizing_ok
    assert result.pressure_loss_ok
    assert result.has_pressure_loss
    assert result.has_warnings
    assert not result.has_errors


def test_section_compute_result_error_helpers() -> None:
    error = EngineMessage.error(
        code="TEST_ERROR",
        text="Test error.",
        context={"section_id": "S1"},
    )

    result = DomesticWaterSectionComputeResult(
        section_id="S1",
        sizing=SimpleNamespace(has_errors=True),
        pressure_loss=None,
        messages=(error,),
    )

    assert not result.sizing_ok
    assert not result.pressure_loss_ok
    assert not result.has_pressure_loss
    assert not result.has_warnings
    assert result.has_errors


def test_network_compute_result_count_helpers() -> None:
    sized = DomesticWaterSectionComputeResult(
        section_id="S1",
        sizing=SimpleNamespace(has_errors=False),
        pressure_loss=SimpleNamespace(has_errors=False),
    )
    failed = DomesticWaterSectionComputeResult(
        section_id="S2",
        sizing=SimpleNamespace(has_errors=True),
        pressure_loss=None,
    )

    result = DomesticWaterNetworkComputeResult(
        side=DomesticWaterSide.COLD_WATER,
        section_results={
            "S1": sized,
            "S2": failed,
        },
    )

    assert result.section_count == 2
    assert result.sized_section_count == 1
    assert result.pressure_loss_section_count == 1
    assert not result.has_pressure_propagation
    assert not result.has_pressure_summary
    assert not result.has_warnings
    assert not result.has_errors