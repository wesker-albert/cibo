"""A Room is a space that exists within the world, and which players and NPCs can
occupy as well as navigate through.

This is a collection of all the rooms that exist in the world.
"""

from typing import List

from cibo.exception import RoomNotFound
from cibo.models import Direction, Room, RoomDescription, RoomExit, RoomFlag
from cibo.resources.__resource__ import Resource
from cibo.resources.sectors import Sectors


class Rooms(Resource):
    """All the rooms that exist in the world."""

    def __init__(self, rooms_file: str, sectors: Sectors):
        self._sectors = sectors
        self._rooms: List[Room] = self._generate_resources(rooms_file)

    def _create_resource_from_dict(self, resource: dict) -> Room:
        """Takes an individual room in raw dict format, and constructs a room out of it.

        Args:
            resource (dict): The room as a raw dict.

        Returns:
            Room: The fully constructed room.
        """

        room = resource

        return Room(
            id_=room["id"],
            name=room["name"],
            description=RoomDescription(
                normal=room["description"]["normal"],
                extra=room["description"].get("extra", None),
                night=room["description"].get("night", None),
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
            sector=self._sectors.get_by_id(room["sector_id"]),
            flags=[RoomFlag(flag) for flag in room["flags"]],
        )

    def get_by_id(self, id_: int) -> Room:
        """Get a room by its ID.

        Args:
            id_ (int): The room ID you're looking for.

        Raises:
            RoomNotFound: No room found for the given ID.

        Returns:
            Room: The matching room.
        """

        for room in self._rooms:
            if room.id_ == id_:
                return room

        raise RoomNotFound
