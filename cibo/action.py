"""Actions module"""


from abc import ABC, abstractmethod
from typing import List

from cibo.models.client import Client
from cibo.password import Password
from cibo.telnet import TelnetServer


class Action(ABC):
    """The base interface used by other action classes."""

    def __init__(self, telnet: TelnetServer) -> None:
        self.telnet = telnet
        self._password_hasher = Password()

    def _join_args(self, args: List[str]) -> str:
        """Join the list of args into a singular string, using a space as the
        delimiter.

        Args:
            args (str): The list of args

        Returns:
            str: All the args as one big string
        """

        return " ".join([str(x) for x in args])

    @abstractmethod
    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action. If no arguments are
        necessary for the action, you should return an empty list.

        Returns:
            List[str]: Descriptions for each required argument
        """

        pass  # pylint: disable=unnecessary-pass

    @abstractmethod
    def process(self, client: Client, args: List[str]) -> None:
        """Process the logic for the action."""

        pass  # pylint: disable=unnecessary-pass


class Say(Action):
    """Contains logic for the 'say' action."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Say something to the current room."""

        for connected_client in self.telnet.get_connected_clients():
            connected_client.send_message(
                f'{client.address} says, "{self._join_args(args)}"'
            )


class Register(Action):
    """Contains logic for the 'register' action."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return ["name", "password"]

    def process(self, client: Client, args: List[str]):
        """Register a new player with the server."""

        if client.is_logged_in:
            client.send_message(
                "If you want to create a new player, you'll need to log out of your "
                "current player session."
            )
            return

        player_name = args[0]
        password = args[1]

        if player_name == "name":
            client.send_message("Please try again with an *actual* name.")
            return

        if player_name == "password":
            client.send_message("Please try again with an *actual* password.")
            return

        client.registration_name = player_name
        client.registration_password_hash = self._password_hasher.hash_(password)

        client.send_message(
            f"Are you sure you want to create the player named {player_name}?\n"
            "Type 'finalize' to finalize the player creation. If you want to use a "
            "different name or password, you can 'register' again.\n"
            "Otherwise, feel free to 'login' to an already existing player."
        )


class Finalize(Action):
    """Contains logic for the 'finalize' action."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Finalizes the creation of a new player."""

        if client.is_logged_in:
            client.send_message(
                "If you want to create a new player, you'll need to log out of your "
                "current player session."
            )
            return

        if not client.registration_name or not client.registration_password_hash:
            client.send_message("You'll need to 'register' before you can 'finalize'.")
            return

        _ = args


class Login(Action):
    """Contains logic for the 'login' action."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return ["name", "password"]

    def process(self, client: Client, args: List[str]):
        """Log in to an existing player on the server."""

        _ = client, args


class Move(Action):
    """Contains logic for movement actions."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Moves a client between available rooms."""

        _ = client, args


class Look(Action):
    """Contains logic for the 'look' action."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return ["direction/item"]

    def process(self, client: Client, args: List[str]):
        """Returns information about the room or object targeted."""

        _ = client, args


class Exits(Action):
    """Contains logic for the 'exits' action."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Returns the available exits."""

        _ = client, args


class Quit(Action):
    """Contains logic for the 'quit' action."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Quits the game and disconnects the client."""

        _ = client, args
