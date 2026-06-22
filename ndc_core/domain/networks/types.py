from __future__ import annotations

from enum import StrEnum
from typing import NewType

CellId = NewType("CellId", str)
NodeId = NewType("NodeId", str)
SectionId = NewType("SectionId", str)


class NetworkKind(StrEnum):
    """Supported network families."""

    COLD_WATER = "cold_water"
    HOT_WATER = "hot_water"
    HOT_WATER_LOOP = "hot_water_loop"
    DRAINAGE = "drainage"
    RAINWATER = "rainwater"
    HEATING = "heating"
    VENTILATION = "ventilation"
    OTHER = "other"


class NodeKind(StrEnum):
    """Topological node kind."""

    SOURCE = "source"
    JUNCTION = "junction"
    TERMINAL = "terminal"
    RISER_BASE = "riser_base"
    RISER_TOP = "riser_top"
    EQUIPMENT = "equipment"
    OTHER = "other"


class SectionUsageContext(StrEnum):
    """Hydraulic context used later by sizing engines."""

    BASEMENT = "basement"
    TECHNICAL_ROOM = "technical_room"
    RISER = "riser"
    DISTRIBUTION = "distribution"
    DWELLING = "dwelling"
    BRANCH = "branch"
    COLLECTOR = "collector"
    LOOP_RETURN = "loop_return"
    OTHER = "other"


class DiameterMode(StrEnum):
    """Indicates whether the diameter is selected or imposed."""

    AUTOMATIC = "automatic"
    FORCED_PIPE = "forced_pipe"
    FORCED_INTERNAL_DIAMETER = "forced_internal_diameter"