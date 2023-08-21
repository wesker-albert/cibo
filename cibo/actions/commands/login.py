"""Log in to an existing player on the server."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.actions.commands.look import Look
from cibo.client import Client
from cibo.exception import (
    ClientIsLoggedIn,
    PasswordIncorrect,
    PlayerNotFound,
    PlayerSessionActive,
)
from cibo.models.data.player import Player
from cibo.models.object.announcement import Announcement


class Login(Action):
    """Log in to an existing player on the server."""

    def aliases(self) -> List[str]:
        return ["login"]

    def required_args(self) -> List[str]:
        return ["name", "password"]

    @property
    def is_logged_in_msg(self) -> str:
        """Player is already logged in."""

        return (
            "You login to Facebook, to make sure your ex isn't doing better than "
            "you are."
        )

    def player_not_found_msg(self, player_name: str) -> str:
        """Player doesn't exist."""

        return (
            f"A player by the name [cyan]{player_name}[/] does not exist. "
            "If you want, you can [green]register[/] a new player with that name."
        )

    @property
    def incorrect_password_msg(self) -> str:
        """Incorrect password entered."""

        return "[bright_red]Incorrect password.[/]"

    def player_session_active_msg(self, player_name: str) -> str:
        """Another Client is already logged into a session with the Player."""

        return (
            f"The player [cyan]{player_name}[/] is already logged in. "
            "If this player belongs to you and you think it's been stolen, please "
            "contact the admin."
        )

    def logging_in_msg(self, player_name: str) -> Announcement:
        """Successfully loggin in."""

        return Announcement(
            "You take the [red]red pill[/]. You have a look around, to see how "
            "deep the rabbit hole goes...",
            f"[cyan]{player_name}[/] falls from heaven. It looks like it hurt.",
        )

    def check_for_player_session(self, name: str) -> None:
        """Checks to see if the Player is already logged into and active session, by
        a different client.

        Args:
            name (str): The Player name to check.

        Returns:
            bool: True if the player is already logged in.
        """

        for client in self._telnet.get_connected_clients():
            if client.is_logged_in and client.player and client.player.name == name:
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
            self.send.private(client, self.is_logged_in_msg)

        except PlayerNotFound:
            self.send.private(client, self.player_not_found_msg(player_name))

        except PasswordIncorrect:
            self.send.private(client, self.incorrect_password_msg)

        except PlayerSessionActive:
            self.send.private(client, self.player_session_active_msg(player_name))

        else:
            client.log_in(player)

            logging_in_msg = self.logging_in_msg(client.player.name)

            self.send.private(client, logging_in_msg.to_self, prompt=False)
            self.send.local(
                client.player.current_room_id, logging_in_msg.to_room, [client]
            )

            Look(self._telnet, self._world, self._output).process(client, None, [])
