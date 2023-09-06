"""An Npc is a non-player character, that a player might encounter while exploring
the world. Some Npcs can be interacted with, in varying ways.
"""

from dataclasses import dataclass

from cibo.models.description import EntityDescription


@dataclass
class Npc:
    """Represents a non-player character."""

    id_: int
    name: str
    description: EntityDescription

    @property
    def room_description(self) -> str:
        return f"{self.name} {self.description.room}".capitalize()
