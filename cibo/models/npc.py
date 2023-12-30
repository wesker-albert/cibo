"""An NPC is a non-player character, that a player might encounter while exploring
the world. Some NPCs can be interacted with, in varying ways.
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
        """The NPC name and room description together, capitalized and in a friendly
        format.

        Returns:
            str: The combined room description.
        """

        return f"{self.name} {self.description.room}".capitalize()
