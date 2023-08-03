"""Finalizes the creation of a new player."""

from sqlite3 import IntegrityError
from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client


class Finalize(Action):
    """Finalizes the creation of a new player."""

    def aliases(self) -> List[str]:
        return ["finalize"]

    def required_args(self) -> List[str]:
        return []

    @property
    def already_logged_in_msg(self) -> str:
        """Player is already logged in."""

        return "You finalize your written will, leaving your whole estate to your cat."

    @property
    def not_registered_msg(self) -> str:
        """Didn't register first."""

        return "You'll need to [green]register[/] before you can [green]finalize[/]."

    def registered_msg(self, player_name: str) -> str:
        """Finalization was successful."""

        return (
            f"[cyan]{player_name}[/] has been created. You can now [green]login[/] "
            "with this player."
        )

    def name_not_available_msg(self, player_name: str) -> str:
        """Player name is already taken."""

        return (
            f"Sorry, turns out the name [cyan]{player_name}[/] is already taken. "
            "Please [green]register[/] again with a different name."
        )

    def process(self, client: Client, _command: str, _args: List[str]) -> None:
        if client.is_logged_in:
            self.send.private(client, self.already_logged_in_msg)
            return

        if not client.registration:
            self.send.private(client, self.not_registered_msg)
            return

        try:
            client.registration.save()

            self.send.private(client, self.registered_msg(client.registration.name))

        # a Player with the same name already exists
        except IntegrityError:
            self.send.private(
                client, self.name_not_available_msg(client.registration.name)
            )

        client.registration = None
