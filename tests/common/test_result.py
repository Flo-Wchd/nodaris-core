from ndc_core.common.errors import ManagedError
from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.common.status import ResultStatus


def test_success_result_without_message() -> None:
    result = Result.success(value=42)

    assert result.ok
    assert not result.failed
    assert result.value == 42
    assert result.status is ResultStatus.SUCCESS
    assert not result.has_messages
    assert not result.has_warnings
    assert not result.has_errors


def test_success_result_with_warning_becomes_partial() -> None:
    result = Result.success(value=42).with_message(
        EngineMessage.warning(
            code="CORE_WARNING",
            text="Warning message.",
        )
    )

    assert result.ok
    assert not result.failed
    assert result.status is ResultStatus.PARTIAL
    assert result.has_messages
    assert result.has_warnings
    assert not result.has_errors
    assert len(result.warnings) == 1


def test_result_with_error_becomes_failure() -> None:
    result = Result.success(value=42).with_message(
        EngineMessage.error(
            code="CORE_ERROR",
            text="Error message.",
        )
    )

    assert not result.ok
    assert result.failed
    assert result.status is ResultStatus.FAILURE
    assert result.has_errors
    assert len(result.errors) == 1


def test_failure_result() -> None:
    result = Result.failure(
        messages=[
            EngineMessage.error(
                code="CORE_FAILURE",
                text="Failure message.",
            )
        ]
    )

    assert not result.ok
    assert result.failed
    assert result.value is None
    assert result.status is ResultStatus.FAILURE
    assert result.has_errors


def test_result_with_value_returns_new_result() -> None:
    result = Result.success(value=1)
    updated = result.with_value(2)

    assert result.value == 1
    assert updated.value == 2
    assert updated.status is ResultStatus.SUCCESS


def test_managed_error_to_message() -> None:
    managed_error = ManagedError(
        code="CORE_MANAGED_ERROR",
        text="Managed error.",
        context={"field": "diameter_mm"},
    )

    message = managed_error.to_message()

    assert message.is_error
    assert message.code == "CORE_MANAGED_ERROR"
    assert message.text == "Managed error."
    assert message.context["field"] == "diameter_mm"