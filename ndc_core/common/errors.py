from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from ndc_core.common.messages import EngineMessage


@dataclass(frozen=True, slots=True)
class ManagedError:
    """
    Non-blocking business error.

    This class represents a managed error that can be converted into an
    EngineMessage and returned inside a Result.
    """

    code: str
    text: str
    context: Mapping[str, Any] = field(default_factory=dict)

    def to_message(self) -> EngineMessage:
        return EngineMessage.error(
            code=self.code,
            text=self.text,
            context=self.context,
        )