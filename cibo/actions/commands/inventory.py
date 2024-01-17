"""Display the itemized contents of the user inventory."""

from typing import List

from cibo.actions._base_ import Action
from cibo.exceptions import ClientNotLoggedIn
from cibo.models.client import Client
from cibo.models.message import Message, MessageRoute


class Inventory(Action):
    """Check what items you're carrying."""

    def aliases(self) -> List[str]:
        return ["inventory", "inv", "i"]

    def required_args(self) -> List[str]:
        return []

    @property
    def _empty_inventory_message(self) -> Message:
        """The user inventory is empty."""

        return Message("You aren't carrying anything...")

    def _inventory_message(self, client: Client) -> Message:
        """The contents of the user inventory."""

        inventory_items = [
            item.name for item in self.items.get_from_dataset(client.user.inventory)
        ]

        inventory = "\n".join([str(item).capitalize() for item in inventory_items])

        return (
            Message(inventory)
            if len(inventory_items) > 0
            else self._empty_inventory_message
        )

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

        except ClientNotLoggedIn:
            self.comms.send_prompt(client)

        else:
            self.comms.send_to_client(
                MessageRoute(self._inventory_message(client), client=client)
            )
