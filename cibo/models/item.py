"""An item is an in-game piece of inventory, that can be picked up, carried, and
often used by a user.
"""

from dataclasses import dataclass

from cibo.models.description import EntityDescription


@dataclass
class Item:
    """Represents an interactive item."""

    id_: int
    name: str
    description: EntityDescription
    is_stationary: bool
    carry_limit: int
    weight: int

    @property
    def room_description(self) -> str:
        """The item name and room description together, capitalized and in a friendly
        format.

        Returns:
            str: The combined room description.
        """

        return f"{self.name} {self.description.room}".capitalize()
