"""A door is an interactive object that separates two adjoining rooms. They can
commonly be opened and closed. Though some may be locked and need a key, or otherwise
be impassible until certain events are triggered.

This is a collection of all the Doors that exist in the world.
"""

from typing import List, Optional

from cibo.models.door import Door, DoorFlag
from cibo.resources.__resource__ import Resource


class Doors(Resource):
    """All the Doors that exist in the world."""

    def __init__(self, doors_file: str):
        self._doors: List[Door] = self._generate_resources(doors_file)

    def _create_resource_from_dict(self, resource: dict) -> Door:
        """Takes an individual Door in raw dict format, and constructs a Door out of it.

        Args:
            resource (dict): The Door as a raw dict.

        Returns:
            Door: The fully constructed Door.
        """

        door = resource

        return Door(
            name=door["name"],
            room_ids=list(door["room_ids"]),
            flags=[DoorFlag(flag) for flag in door.get("flags", [])],
        )

    def get_by_room_ids(self, room_id: int, adjoining_room_id: int) -> Optional[Door]:
        """Get a Door using the two adjoining Room IDs.

        Args:
            room_id (int): The ID of a Room.
            adjoining_room_id (int): The ID of the adjoinging Room.

        Returns:
            Optional[Door]: The Door if, one exists between the two Rooms.
        """

        for door in self._doors:
            if room_id in door.room_ids and adjoining_room_id in door.room_ids:
                return door

        return None
