"""A Room is a space that exists within the world, and which Players and Npcs can
occupy as well as navigate through.

This is a collection of all the Rooms that exist in the world.
"""

from typing import List

from cibo.exception import RoomNotFound
from cibo.models.direction import Direction
from cibo.models.flag import RoomFlag
from cibo.models.room import Room, RoomDescription, RoomExit
from cibo.resources.__resource__ import Resource


class Rooms(Resource):
    """All the Rooms that exist in the world."""

    def __init__(self, rooms_file: str):
        self._rooms: List[Room] = self._generate_resources(rooms_file)

    def _create_resource_from_dict(self, resource: dict) -> Room:
        """Takes an individual Room in raw dict format, and constructs a Room out of it.

        Args:
            resource (dict): The Room as a raw dict.

        Returns:
            Room: The fully constructed Room.
        """

        room = resource

        return Room(
            id_=room["id"],
            name=room["name"],
            description=RoomDescription(
                normal=room["description"]["normal"],
                extra=room["description"].get("extra", None),
                night=room["description"].get("night", None),
                under=room["description"].get("under", None),
                behind=room["description"].get("behind", None),
                above=room["description"].get("above", None),
                smell=room["description"].get("smell", None),
                listen=room["description"].get("listen", None),
            ),
            exits=[
                RoomExit(
                    direction=Direction(exit_["direction"]),
                    id_=exit_["id"],
                    description=exit_.get("description", None),
                )
                for exit_ in room["exits"]
            ],
            flags=[RoomFlag(flag) for flag in room["flags"]],
        )

    def get_by_id(self, id_: int) -> Room:
        """Get a Room by its ID. Returns None if not found.

        Args:
            id_ (int): The Room ID you're looking for.

        Raises:
            RoomNotFound: No room found for the given ID.

        Returns:
            Optional[Room]: The matching Room.
        """

        for room in self._rooms:
            if room.id_ == id_:
                return room

        raise RoomNotFound
