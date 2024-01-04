"""Display the itemized contents of the player inventory."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import ClientNotLoggedIn
from cibo.messages.__message__ import Message


class Inventory(Action):
    """Check what items you're carrying."""

    def aliases(self) -> List[str]:
        return ["inventory", "inv", "i"]

    def required_args(self) -> List[str]:
        return []

    @property
    def empty_inventory_message(self) -> Message:
        """The player inventory is empty."""

        return Message("You aren't carrying anything...")

    def get_formatted_inventory(self, client: Client) -> Message:
        """The contents of the player inventory.

        Args:
            client (Client): The client whose inventory will be checked.

        Returns:
            str: The items in the player inventory.
        """

        inventory_items = [
            item.name for item in self.items.get_from_dataset(client.player.inventory)
        ]

        inventory = "\n".join([str(item).capitalize() for item in inventory_items])

        return (
            Message(inventory)
            if len(inventory_items) > 0
            else self.empty_inventory_message
        )

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

        except ClientNotLoggedIn:
            self.output.send_prompt(client)

        else:
            self.output.send_private_message(
                client, self.get_formatted_inventory(client)
            )
