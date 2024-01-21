"""A Door is an interactive object that separates two adjoining rooms. They can
commonly be opened and closed. Though some may be locked and need a key, or otherwise
be impassible until certain events are triggered.

This is a collection of all the doors that exist in the world.
"""

from typing import List

from cibo.entities import Entity
from cibo.exceptions import DoorNotFound
from cibo.models.door import Door
from cibo.models.flag import DoorFlag


class Doors(Entity):
    """All the doors that exist in the world."""

    def __init__(self, doors_file: str):
        self._doors: List[Door] = self._generate_entities(doors_file)

    def _create_entity_from_dict(self, entity: dict) -> Door:
        """Takes an individual door in raw dict format, and constructs a door out of it.

        Args:
            entity (dict): The door as a raw dict.

        Returns:
            Door: The fully constructed door.
        """

        door = entity

        return Door(
            name=door["name"],
            room_ids=list(door["room_ids"]),
            flags=[DoorFlag(flag) for flag in door.get("flags", [])],
        )

    def get_by_room_ids(self, room_id: int, adjoining_room_id: int) -> Door:
        """Get a door using the two adjoining room IDs.

        Args:
            room_id (int): The ID of a room.
            adjoining_room_id (int): The ID of the adjoining room.

        Raises:
            DoorNotFound: No door exists between the two rooms.

        Returns:
            Door: The matching door.
        """

        for door in self._doors:
            if room_id in door.room_ids and adjoining_room_id in door.room_ids:
                return door

        raise DoorNotFound
