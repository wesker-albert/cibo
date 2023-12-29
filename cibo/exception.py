"""Custom exceptions that can be raised under specific circumstances, to more clearly
convey useful information that is particular to our server.
"""

from typing import List


class ActionMissingArguments(Exception):
    """Raised if not arguments were supplied to an Action."""

    pass


class ClientNotLoggedIn(Exception):
    """Raised if the Client isn't logged into a Player."""

    pass


class ClientIsLoggedIn(Exception):
    """Raised if the Client is already logged into a Player."""

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
    """Raised if an Input event is received, but no actual input text was entered."""

    pass


class ItemNotFound(Exception):
    """Raised if no Item is found with the given ID."""

    pass


class ItemIsStationary(Exception):
    """Raised if the specified item is a stationary."""

    pass


class InventoryItemNotFound(Exception):
    """Raised if no Item with the given name is found in the Player inventory."""

    pass


class NpcNotFound(Exception):
    """Raised if no Npc is found with the given ID."""

    pass


class PasswordIncorrect(Exception):
    """Raised if a given Player password doesn't match the stored hash."""

    pass


class PlayerNotRegistered(Exception):
    """Raised if no Player is yet registered by the client."""

    pass


class PlayerAlreadyExists(Exception):
    """Raised if no a Player already exists with the name given."""

    pass


class PlayerNotFound(Exception):
    """Raised if no Player with the given name is found to exist."""

    pass


class PlayerSessionActive(Exception):
    """Raised if a client is already logged into a session with the Player."""

    pass


class RegionNotFound(Exception):
    """Raised if the given Region ID doesn't exist."""

    pass


class RoomItemNotFound(Exception):
    """Raised if no Item with the given name is found in the current room."""

    pass


class RoomNotFound(Exception):
    """Raised if the player isn't currently in a room."""

    pass


class SectorNotFound(Exception):
    """Raised by if the given Sector ID doesn't exist."""

    pass


class SpawnNotFound(Exception):
    """Raised if a Spawn can't be found for the given parameters."""

    pass


class SpawnTypeUnknown(Exception):
    """Raised if an unknown type of entity is given for a Spawn."""

    pass
