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

    def process(self, client: Client, _command: str, _args: List[str]):
        if client.is_logged_in:
            self._send.private(
                client,
                "You finalize your written will, leaving your whole estate "
                "to your cat.",
            )
            return

        if not client.registration:
            self._send.private(
                client,
                "You'll need to [green]register[/] before you can "
                "[green]finalize[/].",
            )
            return

        try:
            client.registration.save()

            self._send.private(
                client,
                f"[cyan]{client.registration.name}[/] has been created. "
                "You can now [green]login[/] with this player.",
            )

        # a Player with the same name already exists
        except IntegrityError:
            self._send.private(
                client,
                "Sorry, turns out the name "
                f"[cyan]{client.registration.name}[/] is already "
                "taken. Please [green]register[/] again with a different name.",
            )

        client.registration = None
