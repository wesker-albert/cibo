"""A Room is a space that exists within the world, and which Players and Npcs can
occupy as well as navigate through.

This is a collection of all the Rooms that exist in the world.
"""

from typing import List

from cibo.exception import ExitNotFound, RoomNotFound
from cibo.models.object.room import Direction, Room, RoomDescription, RoomExit
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

    def get_by_id(self, id_: int) -> Room:
        """Get a Room by its ID. Returns None if not found.

        Args:
            id_ (int): The Room ID you're looking for.

        Returns:
            Optional[Room]: The matching Room.
        """

        for room in self._rooms:
            if room.id_ == id_:
                return room

        raise RoomNotFound

    def get_exits(self, room: Room) -> List[str]:
        """Get the text values of the exits for the given Room, in alphabetical order.
        Returns empty if the room has no exits.

        Args:
            room (Room): The Room you're looking for exits in.

        Returns:
            List[str]: The Room exits in str format.
        """

        return sorted([exit_.direction.name.lower() for exit_ in room.exits])

    def get_formatted_exits(self, room: Room) -> str:
        """Formats the exits into a pretty, stylized string.

        Args:
            room (Room): The Room to look for exits in.

        Returns:
            str: The formatted exits.
        """

        exits = self.get_exits(room)

        # plurality is important...
        if not exits:
            return "[green]Exits:[/] none"

        if len(exits) == 1:
            return f"[green]Exit:[/] {exits[0]}"

        joined_exits = ", ".join([str(exit_) for exit_ in exits])
        return f"[green]Exits:[/] {joined_exits}"

    def get_direction_exit(self, room: Room, direction: str) -> RoomExit:
        """Returns the Room exit in the direction given, if an exit exists that way.

        Args:
            room (Room): The Room you want to check the exits in.
            direction (str): The direction to check.

        Returns:
            Optional[RoomExit]: The exit, if it exists.
        """

        for exit_ in room.exits:
            if (
                direction == exit_.direction.value
                or direction == exit_.direction.name.lower()
            ):
                return exit_

        raise ExitNotFound
