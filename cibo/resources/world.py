"""The whole world. Or rather, everything that exists within it.
Rooms, Items, Npcs.
"""

from cibo.resources.rooms import Rooms


class World:
    """The whole world. Or rather, everything that exists within it.
    Rooms, Items, Npcs.
    """

    def __init__(self):
        self.rooms = Rooms()
