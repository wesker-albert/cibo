"""Finalizes the creation of a new player."""

from typing import List

from peewee import IntegrityError

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import ClientIsLoggedIn, PlayerAlreadyExists, PlayerNotRegistered
from cibo.models.data.item import Item
from cibo.models.data.player import Player
from cibo.output import Message


class Finalize(Action):
    """Finalizes the creation of a new player."""

    def aliases(self) -> List[str]:
        return ["finalize"]

    def required_args(self) -> List[str]:
        return []

    @property
    def is_logged_in_message(self) -> Message:
        """Player is already logged in."""

        return Message(
            "You finalize your written will, leaving your whole estate to your cat."
        )

    @property
    def not_registered_message(self) -> Message:
        """Didn't register first."""

        return Message(
            "You'll need to [green]register[/] before you can [green]finalize[/]."
        )

    def player_already_exists_message(self, player_name: str) -> Message:
        """Player name is already taken."""

        return Message(
            f"Sorry, turns out the name [cyan]{player_name}[/] is already taken. "
            "Please [green]register[/] again with a different name."
        )

    def successfully_registered_message(self, player_name: str) -> Message:
        """Finalization was successful."""

        return Message(
            f"[cyan]{player_name}[/] has been created. You can now [green]login[/] "
            "with this player."
        )

    def save_player_registration(self, client: Client) -> None:
        """Save the registered player to the database.

        Args:
            client (Client): The client containing the registration info.

        Raises:
            PlayerAlreadyExists: A player with the same name already exists.
        """

        try:
            client.registration.save()

        except IntegrityError as ex:
            raise PlayerAlreadyExists from ex

    def create_player_starting_inventory(self, client: Client) -> None:
        """Give the newly created player any starting items they may need.

        Args:
            client (Client): The client whose new player needs swag.
        """

        # give the player a fork, for now
        item = Item(item_id=1, player_id=client.registration)
        item.save()

    def process(self, client: Client, _command: str, _args: List[str]) -> None:
        try:
            if client.is_logged_in:
                raise ClientIsLoggedIn

            if not client.is_registered:
                raise PlayerNotRegistered

            self.save_player_registration(client)
            self.create_player_starting_inventory(client)

        except ClientIsLoggedIn:
            self.output.send_private_message(client, self.is_logged_in_message)

        except PlayerNotRegistered:
            self.output.send_private_message(client, self.not_registered_message)

        except PlayerAlreadyExists:
            self.output.send_private_message(
                client, self.player_already_exists_message(client.registration.name)
            )

        else:
            self.output.send_private_message(
                client, self.successfully_registered_message(client.registration.name)
            )

        finally:
            client.registration = Player()
