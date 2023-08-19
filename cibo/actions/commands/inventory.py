"""Display the itemized contents of the Player inventory."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import ClientNotLoggedIn


class Inventory(Action):
    """Check what items you're carrying."""

    def aliases(self) -> List[str]:
        return ["inventory", "inv", "i"]

    def required_args(self) -> List[str]:
        return []

    @property
    def empty_inventory_msg(self) -> str:
        """The Player inventory is empty."""

        return "You aren't carrying anything..."

    def get_formatted_inventory(self, client: Client) -> str:
        """The contents of the Player inventory.

        Args:
            client (Client): The client whose inventory will be checked.

        Returns:
            str: The items in the Player inventory.
        """

        inventory_items = [
            self.items.get_by_id(item.item_id).name for item in client.player.inventory
        ]

        inventory = "\n".join([str(item) for item in inventory_items])

        return inventory if len(inventory_items) > 0 else self.empty_inventory_msg

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

        except ClientNotLoggedIn:
            self.send.prompt(client)

        else:
            self.send.private(client, self.get_formatted_inventory(client))
