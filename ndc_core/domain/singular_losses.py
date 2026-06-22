from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Mapping


class SingularLossMethod(StrEnum):
    """Available methods for singular pressure loss calculation."""

    ZETA = "zeta"
    KV = "kv"
    BETA = "beta"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class SingularLoss:
    """
    Singular loss element placed on a network section.

    The hydraulic calculation is not performed here. This class only carries
    domain data required by pressure loss engines.
    """

    code: str
    name: str
    method: SingularLossMethod = SingularLossMethod.ZETA
    zeta: float | None = None
    kv: float | None = None
    quantity: int = 1
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", self.code.strip())
        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "quantity", max(0, self.quantity))

        if self.zeta is not None:
            object.__setattr__(self, "zeta", max(0.0, self.zeta))

        if self.kv is not None:
            object.__setattr__(self, "kv", max(0.0, self.kv))

    @property
    def is_zeta_based(self) -> bool:
        return self.method is SingularLossMethod.ZETA

    @property
    def is_kv_based(self) -> bool:
        return self.method is SingularLossMethod.KV

    @property
    def is_active(self) -> bool:
        return self.quantity > 0