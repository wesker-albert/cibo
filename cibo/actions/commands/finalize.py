"""Finalizes the creation of a new player."""

from sqlite3 import IntegrityError
from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import ClientIsLoggedIn, PlayerAlreadyExists, PlayerNotRegistered
from cibo.models.player import Player


class Finalize(Action):
    """Finalizes the creation of a new player."""

    def aliases(self) -> List[str]:
        return ["finalize"]

    def required_args(self) -> List[str]:
        return []

    @property
    def is_logged_in_msg(self) -> str:
        """Player is already logged in."""

        return "You finalize your written will, leaving your whole estate to your cat."

    @property
    def not_registered_msg(self) -> str:
        """Didn't register first."""

        return "You'll need to [green]register[/] before you can [green]finalize[/]."

    def successfully_registered_msg(self, player_name: str) -> str:
        """Finalization was successful."""

        return (
            f"[cyan]{player_name}[/] has been created. You can now [green]login[/] "
            "with this player."
        )

    def player_already_exists_msg(self, player_name: str) -> str:
        """Player name is already taken."""

        return (
            f"Sorry, turns out the name [cyan]{player_name}[/] is already taken. "
            "Please [green]register[/] again with a different name."
        )

    def save_player_registration(self, client: Client) -> None:
        """Save the registered Player to the database.

        Args:
            client (Client): The client containing the registration info.

        Raises:
            PlayerAlreadyExists: A Player with the same name already exists.
        """

        try:
            client.registration.save()

        except IntegrityError as ex:
            raise PlayerAlreadyExists from ex

    def process(self, client: Client, _command: str, _args: List[str]) -> None:
        try:
            if client.is_logged_in:
                raise ClientIsLoggedIn

            if not client.is_registered:
                raise PlayerNotRegistered

            self.save_player_registration(client)

        except ClientIsLoggedIn:
            self.send.private(client, self.is_logged_in_msg)

        except PlayerNotRegistered:
            self.send.private(client, self.not_registered_msg)

        except PlayerAlreadyExists:
            self.send.private(
                client, self.player_already_exists_msg(client.registration.name)
            )

        else:
            self.send.private(
                client, self.successfully_registered_msg(client.registration.name)
            )

        finally:
            client.registration = Player()
