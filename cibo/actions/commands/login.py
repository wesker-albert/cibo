"""Log in to an existing player on the server."""

from typing import List, Tuple

from cibo.actions import Action
from cibo.actions.commands.look import Look
from cibo.exceptions import (
    ClientIsLoggedIn,
    PasswordIncorrect,
    PlayerNotFound,
    PlayerSessionActive,
)
from cibo.models.client import Client
from cibo.models.data.player import Player
from cibo.models.message import Message, MessageRoute


class Login(Action):
    """Log in to an existing player on the server."""

    def aliases(self) -> List[str]:
        return ["login"]

    def required_args(self) -> List[str]:
        return ["name", "password"]

    @property
    def _is_logged_in_message(self) -> Message:
        """Player is already logged in."""

        return Message(
            "You login to Facebook, to make sure your ex isn't doing better than "
            "you are."
        )

    def _player_not_found_message(self, player_name: str) -> Message:
        """Player doesn't exist."""

        return Message(
            f"A player by the name [cyan]{player_name}[/] does not exist. "
            "If you want, you can [green]register[/] a new player with that name."
        )

    @property
    def _incorrect_password_message(self) -> Message:
        """Incorrect password entered."""

        return Message("[bright_red]Incorrect password.[/]")

    def _player_session_active_message(self, player_name: str) -> Message:
        """Another client is already logged into a session with the player."""

        return Message(
            f"The player [cyan]{player_name}[/] is already logged in. "
            "If this player belongs to you and you think it's been stolen, please "
            "contact the admin."
        )

    def _logging_in_message(self, player_name: str) -> Tuple[Message, Message]:
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

    def _check_for_player_session(self, player_name: str) -> None:
        """Checks to see if the player is already logged into an active session, by
        a different client.

        Args:
            player_name (str): The player name to check.

        Raises:
            PlayerSessionActive: There currently exists an active player session.
        """

        for client in self._telnet.get_connected_clients():
            if client.is_logged_in and client.player.name == player_name:
                raise PlayerSessionActive

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if client.is_logged_in:
                raise ClientIsLoggedIn

            player_name = args[0]
            password = args[1]

            player = Player.get_by_name(player_name)

            self._password_hasher.verify(password, player.password)
            self._check_for_player_session(player.name)

        except ClientIsLoggedIn:
            self.comms.send_to_client(
                MessageRoute(self._is_logged_in_message, client=client)
            )

        except PlayerNotFound:
            self.comms.send_to_client(
                MessageRoute(self._player_not_found_message(player_name), client=client)
            )

        except PasswordIncorrect:
            self.comms.send_to_client(
                MessageRoute(self._incorrect_password_message, client=client)
            )

        except PlayerSessionActive:
            self.comms.send_to_client(
                MessageRoute(
                    self._player_session_active_message(player_name), client=client
                )
            )

        else:
            client.log_in(player)

            logging_in_message = self._logging_in_message(client.player.name)

            self.comms.send_to_vicinity(
                MessageRoute(logging_in_message[0], client=client, send_prompt=False),
                MessageRoute(
                    logging_in_message[1], ids=[client.player.current_room_id]
                ),
            )

            Look(self._server_config).process(client, None, [])
