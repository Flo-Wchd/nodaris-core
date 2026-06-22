from ndc_core.common.messages import EngineMessage
from ndc_core.common.status import MessageSeverity


def test_engine_message_info_factory() -> None:
    message = EngineMessage.info(
        code="CORE_INFO",
        text="Information message.",
        context={"section_id": "S1"},
    )

    assert message.code == "CORE_INFO"
    assert message.text == "Information message."
    assert message.severity is MessageSeverity.INFO
    assert message.is_info
    assert not message.is_warning
    assert not message.is_error
    assert message.context["section_id"] == "S1"


def test_engine_message_warning_factory() -> None:
    message = EngineMessage.warning(
        code="CORE_WARNING",
        text="Warning message.",
    )

    assert message.code == "CORE_WARNING"
    assert message.severity is MessageSeverity.WARNING
    assert message.is_warning


def test_engine_message_error_factory() -> None:
    message = EngineMessage.error(
        code="CORE_ERROR",
        text="Error message.",
    )

    assert message.code == "CORE_ERROR"
    assert message.severity is MessageSeverity.ERROR
    assert message.is_error


def test_engine_message_normalizes_empty_code() -> None:
    message = EngineMessage.info(code="", text="Message without explicit code.")

    assert message.code == "UNKNOWN"


def test_engine_message_to_dict() -> None:
    message = EngineMessage.warning(
        code="CORE_WARNING",
        text="Warning message.",
        context={"node_id": "N1"},
    )

    assert message.to_dict() == {
        "code": "CORE_WARNING",
        "text": "Warning message.",
        "severity": "warning",
        "context": {"node_id": "N1"},
    }