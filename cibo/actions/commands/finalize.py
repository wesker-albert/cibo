"""Finalizes the creation of a new user."""

from typing import List

from peewee import IntegrityError

from cibo.actions._base_ import Action
from cibo.exceptions import ClientIsLoggedIn, UserAlreadyExists, UserNotRegistered
from cibo.models.client import Client
from cibo.models.data.item import Item
from cibo.models.data.user import User
from cibo.models.message import Message, MessageRoute


class Finalize(Action):
    """Finalizes the creation of a new user."""

    def aliases(self) -> List[str]:
        return ["finalize"]

    def required_args(self) -> List[str]:
        return []

    @property
    def _is_logged_in_message(self) -> Message:
        """User is already logged in."""

        return Message(
            "You finalize your written will, leaving your whole estate to your cat."
        )

    @property
    def _not_registered_message(self) -> Message:
        """Didn't register first."""

        return Message(
            "You'll need to [green]register[/] before you can [green]finalize[/]."
        )

    def _user_already_exists_message(self, user_name: str) -> Message:
        """User name is already taken."""

        return Message(
            f"Sorry, turns out the name [cyan]{user_name}[/] is already taken. "
            "Please [green]register[/] again with a different name."
        )

    def _successfully_registered_message(self, user_name: str) -> Message:
        """Finalization was successful."""

        return Message(
            f"[cyan]{user_name}[/] has been created. You can now [green]login[/] "
            "with this user."
        )

    def _save_user_registration(self, client: Client) -> None:
        """Save the registered user to the database.

        Args:
            client (Client): The client containing the registration info.

        Raises:
            UserAlreadyExists: A user with the same name already exists.
        """

        try:
            client.registration.save()

        except IntegrityError as ex:
            raise UserAlreadyExists from ex

    def _create_user_starting_inventory(self, client: Client) -> None:
        """Give the newly created user any starting items they may need.

        Args:
            client (Client): The client whose new user needs swag.
        """

        # give the user a fork, for now
        item = Item(item_id=1, user_id=client.registration)
        item.save()

    def process(self, client: Client, _command: str, _args: List[str]) -> None:
        try:
            if client.is_logged_in:
                raise ClientIsLoggedIn

            if not client.is_registered:
                raise UserNotRegistered

            self._save_user_registration(client)
            self._create_user_starting_inventory(client)

        except ClientIsLoggedIn:
            self.comms.send_to_client(
                MessageRoute(self._is_logged_in_message, client=client)
            )

        except UserNotRegistered:
            self.comms.send_to_client(
                MessageRoute(self._not_registered_message, client=client)
            )

        except UserAlreadyExists:
            self.comms.send_to_client(
                MessageRoute(
                    self._user_already_exists_message(client.registration.name),
                    client=client,
                )
            )

        else:
            self.comms.send_to_client(
                MessageRoute(
                    self._successfully_registered_message(client.registration.name),
                    client=client,
                )
            )

        finally:
            client.registration = User()
