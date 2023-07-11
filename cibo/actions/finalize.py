"""Finalize Action"""

from sqlite3 import IntegrityError
from typing import List

from cibo.actions import Action
from cibo.models import Client


class Finalize(Action):
    """Finalizes the creation of a new player."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        if client.is_logged_in:
            client.send_message(
                "If you want to create a new player, you'll need to log out of your "
                "current player session."
            )
            return

        if not client.registration:
            client.send_message("You'll need to 'register' before you can 'finalize'.")
            return

        try:
            client.registration.save()

            client.send_message(
                f"{client.registration.name} has been created. "
                "You can now 'login' with this player."
            )

        except IntegrityError:
            client.send_message(
                f"Sorry, turns out the name '{client.registration.name}' is already "
                "taken.\n"
                "Please 'register' again with a different name."
            )

        client.registration = None
