"""Actions module"""


class Action:
    """Available interactions with the world"""

    def move(self):
        """Moves a client between available rooms"""
        return

    def look(self):
        """Returns information about the room or object targeted"""
        return

    def exits(self):
        """Returns the available exits"""
        return

    def quit_(self):
        """Quits the game and disconnects the client"""
        return

    def spawn(self):
        """Spawns the character into the world"""
        return
