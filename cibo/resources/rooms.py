"""A Room is a space that exists within the world, and which Players and Npcs can
occupy as well as navigate through.

This is a collection of all the Rooms that exist in the world.
"""

from typing import List, Optional

from cibo.models.room import Direction, Room, RoomDescription, RoomExit
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
        )

    def get(self, id_: int) -> Optional[Room]:
        """Get a Room by its ID. Returns None if not found.

        Args:
            id_ (int): The Room ID you're looking for.

        Returns:
            Optional[Room]: The matching Room.
        """

        for room in self._rooms:
            if room.id_ == id_:
                return room

        return None

    def get_exits(self, id_: int) -> List[str]:
        """Get the text values of the exits for the given Room, in alphabetical order.
        Returns empty if no room by that ID exists, or if the room has no exits.

        Args:
            id_ (int): The Room ID you're looking for.

        Returns:
            List[str]: The Room exits in str format.
        """

        room = self.get(id_)

        if not room:
            return []

        return sorted([exit_.direction.name.lower() for exit_ in room.exits])
