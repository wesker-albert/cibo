"""Custom exceptions that can be raised under specific circumstances, to more clearly
convey useful information that is particular to our server.
"""

from typing import List


class ActionMissingArguments(Exception):
    """Raised if not arguments were supplied to an action."""

    pass


class ClientNotLoggedIn(Exception):
    """Raised if the client isn't logged into a player."""

    pass


class ClientIsLoggedIn(Exception):
    """Raised if the client is already logged into a player."""

    pass


class CommandUnrecognized(Exception):
    """Raised if the client's command is unrecognized.

    Args:
        command (str): The command the client sent.
    """

    def __init__(self, command: str):
        self.message = f"Unrecognized command: {command}"


class CommandMissingArguments(Exception):
    """Raised if the client's command is missing expected arguments.

    Args:
        command (str): The command the client sent.
        required_args (List[str]): Descriptions of the required args for the command.
    """

    def __init__(self, command: str, required_args: List[str]):
        joined_args = " ".join([str(x) for x in required_args])

        self.message = (
            "Command is missing required arguments.\n"
            f"Expected syntax: [green]{command} {joined_args}[/]"
        )


class DoorNotFound(Exception):
    """Raised if there's no door in the direction specified."""

    pass


class DoorIsClosed(Exception):
    """Raised if the door specified is closed."""

    pass


class DoorIsOpen(Exception):
    """Raised if if the door specified is open."""

    pass


class DoorIsLocked(Exception):
    """Raised if the door specified is locked."""

    pass


class ExitNotFound(Exception):
    """Raised if there's no exit in the direction specified."""

    pass


class InputNotReceived(Exception):
    """Raised if an input event is received, but no actual input text was entered."""

    pass


class ItemNotFound(Exception):
    """Raised if no item is found with the given ID."""

    pass


class ItemIsStationary(Exception):
    """Raised if the specified item is a stationary."""

    pass


class InventoryItemNotFound(Exception):
    """Raised if no item with the given name is found in the player inventory."""

    pass


class NpcNotFound(Exception):
    """Raised if no NPC is found with the given ID."""

    pass


class PasswordIncorrect(Exception):
    """Raised if a given player password doesn't match the stored hash."""

    pass


class PlayerNotRegistered(Exception):
    """Raised if no player is yet registered by the client."""

    pass


class PlayerAlreadyExists(Exception):
    """Raised if no a player already exists with the name given."""

    pass


class PlayerNotFound(Exception):
    """Raised if no player with the given name is found to exist."""

    pass


class PlayerSessionActive(Exception):
    """Raised if a client is already logged into a session with the player."""

    pass


class RegionNotFound(Exception):
    """Raised if the given region ID doesn't exist."""

    pass


class RoomItemNotFound(Exception):
    """Raised if no item with the given name is found in the current room."""

    pass


class RoomNotFound(Exception):
    """Raised if the player isn't currently in a room."""

    pass


class SectorNotFound(Exception):
    """Raised by if the given sector ID doesn't exist."""

    pass


class SpawnNotFound(Exception):
    """Raised if a spawn can't be found for the given parameters."""

    pass


class SpawnTypeUnknown(Exception):
    """Raised if an unknown type of entity is given for a spawn."""

    pass
