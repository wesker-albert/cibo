"""Log in to an existing player on the server."""

from typing import List, Tuple

from cibo.actions.__action__ import Action
from cibo.actions.commands.look import Look
from cibo.client import Client
from cibo.exception import (
    ClientIsLoggedIn,
    PasswordIncorrect,
    PlayerNotFound,
    PlayerSessionActive,
)
from cibo.messages.__message__ import Message, MessageRoute
from cibo.models.data.player import Player


class Login(Action):
    """Log in to an existing player on the server."""

    def aliases(self) -> List[str]:
        return ["login"]

    def required_args(self) -> List[str]:
        return ["name", "password"]

    @property
    def is_logged_in_message(self) -> Message:
        """Player is already logged in."""

        return Message(
            "You login to Facebook, to make sure your ex isn't doing better than "
            "you are."
        )

    def player_not_found_message(self, player_name: str) -> Message:
        """Player doesn't exist."""

        return Message(
            f"A player by the name [cyan]{player_name}[/] does not exist. "
            "If you want, you can [green]register[/] a new player with that name."
        )

    @property
    def incorrect_password_message(self) -> Message:
        """Incorrect password entered."""

        return Message("[bright_red]Incorrect password.[/]")

    def player_session_active_message(self, player_name: str) -> Message:
        """Another client is already logged into a session with the player."""

        return Message(
            f"The player [cyan]{player_name}[/] is already logged in. "
            "If this player belongs to you and you think it's been stolen, please "
            "contact the admin."
        )

    def logging_in_message(self, player_name: str) -> Tuple[Message, Message]:
        """Successfully loggin in."""

        return (
            Message(
                "You take the [red]red pill[/]. You have a look around, to see how "
                "deep the rabbit hole goes..."
            ),
            Message(
                f"[cyan]{player_name}[/] falls from heaven. It looks like it hurt."
            ),
        )

    def check_for_player_session(self, name: str) -> None:
        """Checks to see if the player is already logged into an active session, by
        a different client.

        Args:
            name (str): The player name to check.

        Returns:
            bool: True if the player is already logged in.
        """

        for client in self._telnet.get_connected_clients():
            if client.is_logged_in and client.player.name == name:
                raise PlayerSessionActive

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if client.is_logged_in:
                raise ClientIsLoggedIn

            player_name = args[0]
            password = args[1]

            player = Player.get_by_name(player_name)

            self._password_hasher.verify(password, player.password)
            self.check_for_player_session(player.name)

        except ClientIsLoggedIn:
            self.output.send_private_message(client, self.is_logged_in_message)

        except PlayerNotFound:
            self.output.send_private_message(
                client, self.player_not_found_message(player_name)
            )

        except PasswordIncorrect:
            self.output.send_private_message(client, self.incorrect_password_message)

        except PlayerSessionActive:
            self.output.send_private_message(
                client, self.player_session_active_message(player_name)
            )

        else:
            client.log_in(player)

            logging_in_message = self.logging_in_message(client.player.name)

            self.output.send_vicinity_message(
                client,
                logging_in_message[0],
                MessageRoute(client.player.current_room_id, logging_in_message[1]),
            )

            Look(self._server_config).process(client, None, [])
