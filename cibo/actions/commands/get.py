"""Picks up an item from the player's current room, and adds it to the player
inventory.
"""

from typing import List, Tuple

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import (
    ActionMissingArguments,
    ClientNotLoggedIn,
    ItemIsStationary,
    ItemNotFound,
    RoomItemNotFound,
)
from cibo.messages.__message__ import Message, MessageRoute
from cibo.models.data.item import Item


class Get(Action):
    """Pick up an item from the current room."""

    def aliases(self) -> List[str]:
        return ["get"]

    def required_args(self) -> List[str]:
        return []

    @property
    def missing_args_message(self) -> Message:
        """No arguments were provided."""

        return Message("You don't get it, and you probably never will.")

    @property
    def room_item_not_found_message(self) -> Message:
        """The given item name isn't in the room."""

        return Message("You look around, but don't see that.")

    @property
    def room_item_is_stationary_message(self) -> Message:
        """The specified item can't be picked up."""

        return Message("You try, but you can't take that.")

    def gotten_item_message(
        self, player_name: str, item_name: str
    ) -> Tuple[Message, Message]:
        """Player has just picked up an item."""

        return (
            Message(f"You pick up {item_name}."),
            Message(f"[cyan]{player_name}[/] picks up {item_name}."),
        )

    def find_item_in_room(self, client: Client, item_name: str) -> Item:
        """Locate the item in the current room, if it exists.

        Args:
            client (Client): The client whose room should be checked.
            item_name (str): The item name, full or partial.

        Raises:
            RoomItemNotFound: The given item name wasn't found in the current room.

        Returns:
            Item: The item entry from the database.
        """

        room_items = Item.get_by_current_room_id(client.player.current_room_id)

        for item in room_items:
            item_meta = self.items.get_by_id(item.item_id)
            if item_name in item_meta.name:
                return item

        raise RoomItemNotFound

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

            if not args:
                raise ActionMissingArguments

            item = self.find_item_in_room(client, self._join_args(args))
            item_meta = self.items.get_by_id(item.item_id)

            if item_meta.is_stationary:
                raise ItemIsStationary

            item.current_room_id = None
            item.player_id = client.player
            item.save()

            gotten_item_message = self.gotten_item_message(
                client.player.name, item_meta.name
            )

            self.output.send_vicinity_message(
                client,
                gotten_item_message[0],
                MessageRoute(client.player.current_room_id, gotten_item_message[1]),
            )

        except (ClientNotLoggedIn, ItemNotFound):
            self.output.send_prompt(client)

        except ActionMissingArguments:
            self.output.send_private_message(client, self.missing_args_message)

        except RoomItemNotFound:
            self.output.send_private_message(client, self.room_item_not_found_message)

        except ItemIsStationary:
            self.output.send_private_message(
                client, self.room_item_is_stationary_message
            )
