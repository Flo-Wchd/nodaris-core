from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from ndc_core.common.status import MessageSeverity


@dataclass(frozen=True, slots=True)
class EngineMessage:
    """
    Managed message returned by core services and calculation engines.

    The core must not interrupt the program with blocking exceptions during
    normal business computations. Instead, engines should return messages
    describing warnings, invalid inputs, missing data or calculation failures.
    """

    code: str
    text: str
    severity: MessageSeverity = MessageSeverity.INFO
    context: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        normalized_code = self.code.strip() if self.code else "UNKNOWN"
        normalized_text = self.text.strip() if self.text else ""

        object.__setattr__(self, "code", normalized_code)
        object.__setattr__(self, "text", normalized_text)

    @classmethod
    def info(
        cls,
        code: str,
        text: str,
        context: Mapping[str, Any] | None = None,
    ) -> EngineMessage:
        return cls(
            code=code,
            text=text,
            severity=MessageSeverity.INFO,
            context=context or {},
        )

    @classmethod
    def warning(
        cls,
        code: str,
        text: str,
        context: Mapping[str, Any] | None = None,
    ) -> EngineMessage:
        return cls(
            code=code,
            text=text,
            severity=MessageSeverity.WARNING,
            context=context or {},
        )

    @classmethod
    def error(
        cls,
        code: str,
        text: str,
        context: Mapping[str, Any] | None = None,
    ) -> EngineMessage:
        return cls(
            code=code,
            text=text,
            severity=MessageSeverity.ERROR,
            context=context or {},
        )

    @property
    def is_info(self) -> bool:
        return self.severity is MessageSeverity.INFO

    @property
    def is_warning(self) -> bool:
        return self.severity is MessageSeverity.WARNING

    @property
    def is_error(self) -> bool:
        return self.severity is MessageSeverity.ERROR

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "text": self.text,
            "severity": self.severity.value,
            "context": dict(self.context),
        }