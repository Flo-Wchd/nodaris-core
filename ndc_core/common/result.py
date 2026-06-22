from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Iterable, TypeVar

from ndc_core.common.messages import EngineMessage
from ndc_core.common.status import MessageSeverity, ResultStatus

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Result(Generic[T]):
    """
    Standard result returned by core services and engines.

    A result contains:
    - an optional value;
    - a global status;
    - zero or more managed messages.

    This object is intentionally immutable. Methods such as ``with_message``
    return a new Result instance.
    """

    value: T | None = None
    status: ResultStatus = ResultStatus.SUCCESS
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @classmethod
    def success(
        cls,
        value: T | None = None,
        messages: Iterable[EngineMessage] = (),
    ) -> Result[T]:
        return cls(
            value=value,
            status=_status_from_messages(messages, default=ResultStatus.SUCCESS),
            messages=tuple(messages),
        )

    @classmethod
    def partial(
        cls,
        value: T | None = None,
        messages: Iterable[EngineMessage] = (),
    ) -> Result[T]:
        return cls(
            value=value,
            status=_status_from_messages(messages, default=ResultStatus.PARTIAL),
            messages=tuple(messages),
        )

    @classmethod
    def failure(
        cls,
        messages: Iterable[EngineMessage] = (),
        value: T | None = None,
    ) -> Result[T]:
        return cls(
            value=value,
            status=ResultStatus.FAILURE,
            messages=tuple(messages),
        )

    @property
    def ok(self) -> bool:
        return self.status is not ResultStatus.FAILURE

    @property
    def failed(self) -> bool:
        return self.status is ResultStatus.FAILURE

    @property
    def has_messages(self) -> bool:
        return bool(self.messages)

    @property
    def has_warnings(self) -> bool:
        return any(message.severity is MessageSeverity.WARNING for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.severity is MessageSeverity.ERROR for message in self.messages)

    @property
    def errors(self) -> tuple[EngineMessage, ...]:
        return tuple(message for message in self.messages if message.is_error)

    @property
    def warnings(self) -> tuple[EngineMessage, ...]:
        return tuple(message for message in self.messages if message.is_warning)

    def with_message(self, message: EngineMessage) -> Result[T]:
        messages = (*self.messages, message)
        return Result(
            value=self.value,
            status=_status_from_messages(messages, default=self.status),
            messages=messages,
        )

    def with_messages(self, messages: Iterable[EngineMessage]) -> Result[T]:
        next_messages = (*self.messages, *tuple(messages))
        return Result(
            value=self.value,
            status=_status_from_messages(next_messages, default=self.status),
            messages=next_messages,
        )

    def with_value(self, value: T | None) -> Result[T]:
        return Result(
            value=value,
            status=self.status,
            messages=self.messages,
        )


def _status_from_messages(
    messages: Iterable[EngineMessage],
    default: ResultStatus,
) -> ResultStatus:
    severities = tuple(message.severity for message in messages)

    if MessageSeverity.ERROR in severities:
        return ResultStatus.FAILURE

    if MessageSeverity.WARNING in severities:
        return ResultStatus.PARTIAL

    return default