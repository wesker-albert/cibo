"""Drops an item from the player's inventory, onto the ground of the current room."""

from typing import List, Tuple

from cibo.actions import Action
from cibo.exceptions import (
    ActionMissingArguments,
    ClientNotLoggedIn,
    InventoryItemNotFound,
    ItemNotFound,
)
from cibo.models.client import Client
from cibo.models.data.item import Item
from cibo.models.message import Message, MessageRoute


class Drop(Action):
    """Drop an item currently in your inventory."""

    def aliases(self) -> List[str]:
        return ["drop"]

    def required_args(self) -> List[str]:
        return []

    @property
    def _missing_args_message(self) -> Message:
        """No arguments were provided."""

        return Message("Drop what? Your pants? No way!")

    @property
    def _inventory_item_not_found_message(self) -> Message:
        """The given item name isn't in the player inventory."""

        return Message("You scour your inventory, but can't find that.")

    def _dropped_item_message(
        self, player_name: str, item_name: str
    ) -> Tuple[Message, Message]:
        """Player has just dropped an item."""

        return (
            Message(f"You drop {item_name}."),
            Message(f"[cyan]{player_name}[/] drops {item_name}."),
        )

    def _find_item_in_inventory(self, client: Client, item_name: str) -> Item:
        """Locate the item in the inventory, if it exists there.

        Args:
            client (Client): The client whose inventory should be checked.
            item_name (str): The item name, full or partial.

        Raises:
            InventoryItemNotFound: The given item name wasn't found in player inventory.

        Returns:
            Item: The item entry from the database.
        """

        inventory: List[Item] = client.player.inventory

        for inventory_item in inventory:
            item_meta = self.items.get_by_id(inventory_item.item_id)
            if item_name in item_meta.name:
                return inventory_item

        raise InventoryItemNotFound

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

            if not args:
                raise ActionMissingArguments

            item = self._find_item_in_inventory(client, self._join_args(args))
            item_meta = self.items.get_by_id(item.item_id)

            item.current_room_id = client.player.current_room_id
            item.player_id = None
            item.save()

            dropped_item_message = self._dropped_item_message(
                client.player.name, item_meta.name
            )

            self.comms.send_to_vicinity(
                MessageRoute(dropped_item_message[0], client=client),
                MessageRoute(
                    dropped_item_message[1], ids=[client.player.current_room_id]
                ),
            )

        except (ClientNotLoggedIn, ItemNotFound):
            self.comms.send_prompt(client)

        except ActionMissingArguments:
            self.comms.send_to_client(
                MessageRoute(self._missing_args_message, client=client)
            )

        except InventoryItemNotFound:
            self.comms.send_to_client(
                MessageRoute(self._inventory_item_not_found_message, client=client)
            )
