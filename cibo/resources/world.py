"""The whole world. Or rather, everything that exists within it.
Rooms, Items, Npcs.
"""

from os import getenv
from pathlib import Path

from cibo.resources.doors import Doors
from cibo.resources.items import Items
from cibo.resources.rooms import Rooms


class World:
    """The whole world. Or rather, everything that exists within it.
    Rooms, Items, Npcs, etc.
    """

    def __init__(self) -> None:
        self.rooms = Rooms(getenv("ROOMS_PATH", "/cibo/resources/rooms.json"))
        self.doors = Doors(getenv("DOORS_PATH", "/cibo/resources/doors.json"))
        self.items = Items(getenv("ITEMS_PATH", "/cibo/resources/items.json"))

    @property
    def motd(self) -> str:
        """Gets an MOTD from a text file, for display when clients connect to the
        server,

        Returns:
            str: The MOTD text.
        """

        motd_path = getenv("MOTD_PATH", "/cibo/resources/motd.txt")

        with open(f"{Path.cwd()}{motd_path}", encoding="utf-8") as file:
            motd = file.read()

        return motd
