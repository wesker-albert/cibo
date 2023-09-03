"""An Npc is a non-player character, that a player might encounter while exploring
the world. Some Npcs can be interacted with, in varying ways.
"""

from dataclasses import dataclass


@dataclass
class NpcDescription:
    """Descriptions of the Npc depending on context."""

    room: str
    look: str


@dataclass
class Npc:
    """Represents a non-player character."""

    id_: int
    name: str
    description: NpcDescription
