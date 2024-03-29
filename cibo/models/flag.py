"""Flags are used to ascribe various qualities or behaviors to rooms, items, and
entities in the EntityInterface.
"""

from enum import Enum


class RoomFlag(str, Enum):
    """Indicates that a room, sector, or region should have specific qualities or
    behaviors."""

    INSIDE = "inside"
    OUTSIDE = "outside"


class DoorFlag(str, Enum):
    """States a door or object can be in."""

    OPEN = "open"
    CLOSED = "closed"
    LOCKED = "locked"
