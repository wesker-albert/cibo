"""Finalizes the creation of a new player."""

from sqlite3 import IntegrityError
from typing import List

from cibo.actions import Action
from cibo.client import Client


class Finalize(Action):
    """Finalizes the creation of a new player."""

    def aliases(self) -> List[str]:
        return ["finalize"]

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, args: List[str]):
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
                "You'll need to #GREEN#register#NOCOLOR# before you can "
                "#GREEN#finalize#NOCLOR#.",
            )
            return

        try:
            client.registration.save()

            self._send.private(
                client,
                f"{client.registration.name} has been created. "
                "You can now #GREEN#login#NOCOLOR# with this player.",
            )

        # a Player with the same name already exists
        except IntegrityError:
            self._send.private(
                client,
                "Sorry, turns out the name "
                f"#MAGENTA#{client.registration.name}#NOCOLOR# is already "
                "taken. Please #GREEN#register#NOCOLOR# again with a different name.",
            )

        client.registration = None
