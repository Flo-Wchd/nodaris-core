from __future__ import annotations

from enum import StrEnum


class MessageSeverity(StrEnum):
    """Severity level for a managed engine message."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class ResultStatus(StrEnum):
    """Global status returned by a computation or service."""

    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"

    @property
    def is_success(self) -> bool:
        return self is ResultStatus.SUCCESS

    @property
    def is_partial(self) -> bool:
        return self is ResultStatus.PARTIAL

    @property
    def is_failure(self) -> bool:
        return self is ResultStatus.FAILURE