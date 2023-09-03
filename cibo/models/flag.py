"""Flags are used to ascribe various qualities or behaviors to rooms, items, and
entities in the World.
"""

from enum import Enum


class RoomFlag(str, Enum):
    """Indicates that a room, sector, or region should have specific qualities or
    behaviors."""

    INSIDE = "inside"
    OUTSIDE = "outside"
