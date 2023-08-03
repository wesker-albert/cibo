"""Custom exceptions that can be raised under specific circumstances, to more clearly
convey useful information that is particular to our server.
"""

from typing import List


class UnrecognizedCommand(Exception):
    """Raised if the client's command is unrecognized."""

    def __init__(self, command: str):
        """Raised if the client's command is unrecognized.

        Args:
            command (str): The command the client sent.
        """

        self.message = f"Unrecognized command: {command}"


class CommandMissingArguments(Exception):
    """Raised if the client's command is missing expected arguments."""

    def __init__(self, command: str, required_args: List[str]):
        """Raised if the client's command is missing expected arguments.

        Args:
            command (str): The command the client sent.
            required_args (List[str]): Descriptions of the required args for the
                command.
        """
        joined_args = " ".join([str(x) for x in required_args])

        self.message = (
            "Command is missing required arguments.\n"
            f"Expected syntax: [green]{command} {joined_args}[/]"
        )


class MissingArguments(Exception):
    """Raised if not arguments were supplied to an Action."""

    pass


class RoomNotFound(Exception):
    """Raised by an Action if the player isn't currently in a room."""

    pass


class ExitNotFound(Exception):
    """Raised by an Action if there's no exit in the direction specified."""

    pass


class DoorNotFound(Exception):
    """Raised by an Action if there's no door in the direction specified."""

    pass


class NotLoggedIn(Exception):
    """Raised by an Action if the Client isn't logged into a Player."""

    pass
