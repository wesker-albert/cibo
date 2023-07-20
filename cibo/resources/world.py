"""The whole world. Or rather, everything that exists within it.
Rooms, Items, Npcs.
"""

from cibo.resources.doors import Doors
from cibo.resources.rooms import Rooms


class World:
    """The whole world. Or rather, everything that exists within it.
    Rooms, Items, Npcs, etc.
    """

    def __init__(self):
        self.rooms = Rooms()
        self.doors = Doors()
