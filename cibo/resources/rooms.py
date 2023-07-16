"""A Room is a space that exists within the world, and which Players and Npcs can
occupy as well as navigate through.

This is a collection of all the Rooms that exist in the world.
"""

import json
from pathlib import Path
from typing import List, Optional

from cibo.models.room import Direction, Room, RoomDescription, RoomExit


class Rooms:
    """All the Rooms that exist in the world."""

    def __init__(self):
        self._rooms_file = "rooms.json"
        self._rooms = self._generate_rooms()

    def _generate_rooms(self) -> List[Room]:
        """Generate all the Rooms, from the local JSON file that houses them,

        Returns:
            List[Room]: Rooms, lots of rooms.
        """

        return [
            self._create_room_from_dict(room) for room in self._get_rooms_from_file()
        ]

    def _get_rooms_from_file(self) -> List[dict]:
        """Loads the JSON file into a dict, then compiles each room object into a list.

        Returns:
            List[dict]: The Rooms in raw dict format.
        """

        path = Path(__file__).parent.resolve()

        with open(f"{path}/{self._rooms_file}", encoding="utf-8") as file:
            room_data = json.load(file)

        return room_data["rooms"]

    def _create_room_from_dict(self, room: dict) -> Room:
        """Takes an individual room in raw dict format, and constructs a Room out of it.

        Args:
            room (dict): The room as a raw dict.

        Returns:
            Room: The fully constructed room.
        """

        return Room(
            id_=room["id"],
            name=room["name"],
            description=RoomDescription(normal=room["description"]["normal"]),
            exits=[
                RoomExit(direction=Direction(exit_["direction"]), id_=exit_["id"])
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
