from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from ndc_core.common.messages import EngineMessage
from ndc_core.common.result import Result
from ndc_core.networks.domestic_water.types import DomesticWaterSide


@dataclass(frozen=True, slots=True)
class DomesticWaterMessageBindingResult:
    """
    Result of binding engine messages to domain entities.

    This does not create hydraulic results. It only exposes already-produced
    EngineMessage objects on Network/Section instances for future GUI/export layers.
    """

    side: DomesticWaterSide
    network_message_count: int
    section_message_counts: dict[str, int]
    messages: tuple[EngineMessage, ...] = field(default_factory=tuple)

    @property
    def has_warnings(self) -> bool:
        return any(message.is_warning for message in self.messages)

    @property
    def has_errors(self) -> bool:
        return any(message.is_error for message in self.messages)


@dataclass(frozen=True, slots=True)
class DomesticWaterMessageBinder:
    """
    Attach compute messages to domain entities in a stable GUI-friendly shape.

    Attached attributes:
    - network.engine_messages
    - network.network_messages
    - section.engine_messages
    - section.section_messages

    The binder is best-effort and never raises for business/UI objects.
    """

    side: DomesticWaterSide
    sections: Mapping[str, Any]
    compute_result: Any
    network: Any | None = None

    def bind(self) -> Result[DomesticWaterMessageBindingResult]:
        binding_messages: list[EngineMessage] = []

        network_messages = _dedupe_messages(
            tuple(getattr(self.compute_result, "messages", ()) or ())
        )
        section_messages = self._collect_section_messages()

        if self.network is not None:
            _safe_set_messages(
                entity=self.network,
                primary_attr="engine_messages",
                secondary_attr="network_messages",
                messages=network_messages,
                warning_context={"entity": "network"},
                binding_messages=binding_messages,
            )

        for section_id, messages in section_messages.items():
            section = self.sections.get(section_id)
            if section is None:
                continue

            _safe_set_messages(
                entity=section,
                primary_attr="engine_messages",
                secondary_attr="section_messages",
                messages=messages,
                warning_context={
                    "entity": "section",
                    "section_id": section_id,
                },
                binding_messages=binding_messages,
            )

        result = DomesticWaterMessageBindingResult(
            side=self.side,
            network_message_count=len(network_messages),
            section_message_counts={
                section_id: len(messages)
                for section_id, messages in section_messages.items()
            },
            messages=tuple(binding_messages),
        )

        if result.has_errors:
            return Result.failure(value=result, messages=binding_messages)

        if result.has_warnings:
            return Result.partial(value=result, messages=binding_messages)

        return Result.success(value=result, messages=binding_messages)

    def _collect_section_messages(self) -> dict[str, tuple[EngineMessage, ...]]:
        section_messages: dict[str, list[EngineMessage]] = {
            str(section_id): []
            for section_id in self.sections
        }

        section_results = getattr(self.compute_result, "section_results", {}) or {}

        for section_id, section_result in section_results.items():
            messages = tuple(getattr(section_result, "messages", ()) or ())
            section_messages.setdefault(str(section_id), []).extend(messages)

        for message in tuple(getattr(self.compute_result, "messages", ()) or ()):
            section_id = _message_section_id(message)
            if not section_id:
                continue

            if section_id not in self.sections:
                continue

            section_messages.setdefault(section_id, []).append(message)

        return {
            section_id: _dedupe_messages(tuple(messages))
            for section_id, messages in section_messages.items()
        }


def bind_domestic_water_messages_to_entities(
    *,
    side: DomesticWaterSide,
    sections: Mapping[str, Any],
    compute_result: Any,
    network: Any | None = None,
) -> Result[DomesticWaterMessageBindingResult]:
    """
    Convenience function for binding domestic water compute messages.
    """

    return DomesticWaterMessageBinder(
        side=side,
        sections=sections,
        compute_result=compute_result,
        network=network,
    ).bind()


def _safe_set_messages(
    *,
    entity: Any,
    primary_attr: str,
    secondary_attr: str,
    messages: tuple[EngineMessage, ...],
    warning_context: dict[str, Any],
    binding_messages: list[EngineMessage],
) -> None:
    for attr_name in (primary_attr, secondary_attr):
        try:
            setattr(entity, attr_name, tuple(messages))
        except (AttributeError, TypeError):
            binding_messages.append(
                EngineMessage.warning(
                    code="DOMESTIC_WATER_MESSAGE_BINDING_SKIPPED",
                    text="Engine messages could not be attached to an entity.",
                    context={
                        **warning_context,
                        "attribute": attr_name,
                    },
                )
            )


def _message_section_id(message: EngineMessage) -> str | None:
    context = getattr(message, "context", None)

    if not isinstance(context, dict):
        return None

    for key in ("section_id", "section", "sectionId"):
        value = context.get(key)
        if value is None:
            continue

        section_id = str(value or "").strip()
        if section_id:
            return section_id

    return None


def _dedupe_messages(messages: tuple[EngineMessage, ...]) -> tuple[EngineMessage, ...]:
    seen: set[tuple[str, str, str, str]] = set()
    deduped: list[EngineMessage] = []

    for message in messages:
        fingerprint = _message_fingerprint(message)

        if fingerprint in seen:
            continue

        seen.add(fingerprint)
        deduped.append(message)

    return tuple(deduped)


def _message_fingerprint(message: EngineMessage) -> tuple[str, str, str, str]:
    severity = str(getattr(message, "severity", "") or "")
    code = str(getattr(message, "code", "") or "")
    text = str(getattr(message, "text", "") or "")
    context = repr(getattr(message, "context", None) or {})

    return severity, code, text, context