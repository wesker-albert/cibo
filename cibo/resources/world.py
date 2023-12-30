"""The whole world. Or rather, everything that exists within it.
Rooms, items, NPCs, etc.
"""

from os import getenv
from pathlib import Path

from cibo.resources.doors import Doors
from cibo.resources.items import Items
from cibo.resources.npcs import Npcs
from cibo.resources.regions import Regions
from cibo.resources.rooms import Rooms
from cibo.resources.sectors import Sectors
from cibo.resources.spawns import Spawns


class World:
    """The whole world. Or rather, everything that exists within it.
    Rooms, items, NPCs, etc.
    """

    def __init__(self) -> None:
        self.regions = Regions(getenv("REGIONS_PATH", "/cibo/config/regions.json"))
        self.sectors = Sectors(
            getenv("SECTORS_PATH", "/cibo/config/sectors.json"), self.regions
        )
        self.rooms = Rooms(
            getenv("ROOMS_PATH", "/cibo/config/rooms.json"), self.sectors
        )
        self.doors = Doors(getenv("DOORS_PATH", "/cibo/config/doors.json"))
        self.items = Items(getenv("ITEMS_PATH", "/cibo/config/items.json"))
        self.npcs = Npcs(getenv("NPCS_PATH", "/cibo/config/npcs.json"))
        self.spawns = Spawns(
            getenv("SPAWNS_PATH", "/cibo/config/spawns.json"), self.items, self.npcs
        )

    @property
    def motd(self) -> str:
        """Gets an MOTD from a text file, for display when clients connect to the
        server,

        Returns:
            str: The MOTD text.
        """

        motd_path = getenv("MOTD_PATH", "/cibo/config/motd.txt")

        with open(f"{Path.cwd()}{motd_path}", encoding="utf-8") as file:
            motd = file.read()

        return motd
