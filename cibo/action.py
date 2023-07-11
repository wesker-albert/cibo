"""Actions module.

Any newly added Action classes will also need to have a Command() map added to the
cibo.command.CommandProcessor _commands() method. Only then will the new Action be
available to clients.
"""


from abc import ABC, abstractmethod
from sqlite3 import IntegrityError
from typing import List

from marshmallow import ValidationError

from cibo.models.client import Client
from cibo.models.player import Player, PlayerSchema
from cibo.password import Password
from cibo.telnet import TelnetServer


class Action(ABC):
    """The base interface used by other action classes."""

    def __init__(self, telnet: TelnetServer) -> None:
        self._telnet = telnet
        self._password_hasher = Password()

    def _join_args(self, args: List[str]) -> str:
        """Join the list of args into a singular string, using a space as the
        delimiter.

        Args:
            args (List[str]): The list of args

        Returns:
            str: All the args as one big string
        """

        return " ".join([str(x) for x in args])

    @abstractmethod
    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action. If no arguments are
        necessary for the action, return an empty list.

        Returns:
            List[str]: Descriptions for each required argument
        """

        pass

    @abstractmethod
    def process(self, client: Client, args: List[str]) -> None:
        """Process the logic for the action.

        Args:
            client (Client): The client who triggered the action
            args (List[str]): The args included with the command maped to the action
        """

        pass


class Say(Action):
    """Say something to the current room."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        for connected_client in self._telnet.get_connected_clients():
            connected_client.send_message(
                f'{client.address} says, "{self._join_args(args)}"'
            )


class Register(Action):
    """Register a new player with the server."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return ["name", "password"]

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        if client.is_logged_in:
            client.send_message(
                "If you want to create a new player, you'll need to log out of your "
                "current player session."
            )
            return

        player_name = args[0]
        password = args[1]

        try:
            Player(name=player_name, password=password).validate(PlayerSchema)

            # a temporary Player model is set on the client, to be created in the db if
            # they call the Finalize action
            client.registration = Player(
                name=player_name, password=self._password_hasher.hash_(password)
            )

            client.send_message(
                f"Are you sure you want to create the player named '{player_name}'?\n"
                "Type 'finalize' to finalize the player creation.\n"
                "If you want to use a different name or password, you can 'register' "
                "again.\n"
                "Otherwise, feel free to 'login' to an already existing player."
            )

        except ValidationError:
            client.send_message(
                "Your player name or password don't meet criteria:\n"
                "* Names must be 3-15 chars and only contain letters, numbers, or "
                "underscores.\n"
                "* Passwords must be minimum 8 chars.\n"
                "Please 'register' again."
            )


class Finalize(Action):
    """Finalizes the creation of a new player."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        if client.is_logged_in:
            client.send_message(
                "If you want to create a new player, you'll need to log out of your "
                "current player session."
            )
            return

        if not client.registration:
            client.send_message("You'll need to 'register' before you can 'finalize'.")
            return

        try:
            client.registration.save()

            client.send_message(
                f"{client.registration.name} has been created. "
                "You can now 'login' with this player."
            )

        except IntegrityError:
            client.send_message(
                f"Sorry, turns out the name '{client.registration.name}' is already "
                "taken.\n"
                "Please 'register' again with a different name."
            )

        client.registration = None


class Login(Action):
    """Log in to an existing player on the server."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return ["name", "password"]

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        _ = client, args


class Move(Action):
    """Moves a client between available rooms."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        _ = client, args


class Look(Action):
    """Returns information about the room or object targeted."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        _ = client, args


class Exits(Action):
    """Returns the available exits."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        _ = client, args


class Quit(Action):
    """Quits the game and disconnects the client."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        _ = client, args
