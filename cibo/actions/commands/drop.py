"""Drops an item from the Player's inventory, onto the ground of the current room."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import (
    ActionMissingArguments,
    ClientNotLoggedIn,
    InventoryItemNotFound,
    ItemNotFound,
)
from cibo.models.data.item import Item
from cibo.models.object.announcement import Announcement


class Drop(Action):
    """Drop an item currently in your inventory."""

    def aliases(self) -> List[str]:
        return ["drop"]

    def required_args(self) -> List[str]:
        return []

    @property
    def missing_args_msg(self) -> str:
        """No arguments were provided."""

        return "Drop what? Your pants? No way!"

    @property
    def inventory_item_not_found_msg(self) -> str:
        """The given item name isn't in the Player inventory."""

        return "You scour your inventory, but can't find that."

    def dropped_item_msg(self, player_name: str, item_name: str) -> Announcement:
        """Player has just dropped an item."""

        return Announcement(
            f"You drop {item_name}.",
            f"[cyan]{player_name}[/] drops {item_name}.",
        )

    def find_item_in_inventory(self, client: Client, item_name: str) -> Item:
        """Locate the item in the inventory, if it exists there.

        Args:
            client (Client): The client whose inventory should be checked.
            item_name (str): The item name, full or partial.

        Raises:
            InventoryItemNotFound: The given item name wasn't found in Player inventory.

        Returns:
            Item: The Item entry from the database.
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

            item = self.find_item_in_inventory(client, self._join_args(args))
            item_meta = self.items.get_by_id(item.item_id)

            item.room_id = client.player.current_room_id
            item.player_id = None
            item.save()

            dropped_item_msg = self.dropped_item_msg(client.player.name, item_meta.name)

            self.send.private(client, dropped_item_msg.to_self)
            self.send.local(
                client.player.current_room_id, dropped_item_msg.to_room, [client]
            )

        except (ClientNotLoggedIn, ItemNotFound):
            self.send.prompt(client)

        except ActionMissingArguments:
            self.send.private(client, self.missing_args_msg)

        except InventoryItemNotFound:
            self.send.private(client, self.inventory_item_not_found_msg)
