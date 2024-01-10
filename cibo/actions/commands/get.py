"""Picks up an item from the player's current room, and adds it to the player
inventory.
"""

from typing import List, Tuple

from cibo.actions._base_ import Action
from cibo.exceptions import (
    ActionMissingArguments,
    ClientNotLoggedIn,
    ItemIsStationary,
    ItemNotFound,
    RoomItemNotFound,
)
from cibo.models import Client, Message, MessageRoute
from cibo.models.data import Item


class Get(Action):
    """Pick up an item from the current room."""

    def aliases(self) -> List[str]:
        return ["get"]

    def required_args(self) -> List[str]:
        return []

    @property
    def _missing_args_message(self) -> Message:
        """No arguments were provided."""

        return Message("You don't get it, and you probably never will.")

    @property
    def _room_item_not_found_message(self) -> Message:
        """The given item name isn't in the room."""

        return Message("You look around, but don't see that.")

    @property
    def _room_item_is_stationary_message(self) -> Message:
        """The specified item can't be picked up."""

        return Message("You try, but you can't take that.")

    def _get_item_message(
        self, player_name: str, item_name: str
    ) -> Tuple[Message, Message]:
        """Player has just picked up an item."""

        return (
            Message(f"You pick up {item_name}."),
            Message(f"[cyan]{player_name}[/] picks up {item_name}."),
        )

    def _find_item_in_room(self, client: Client, item_name: str) -> Item:
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

            item = self._find_item_in_room(client, self._join_args(args))
            item_meta = self.items.get_by_id(item.item_id)

            if item_meta.is_stationary:
                raise ItemIsStationary

            item.current_room_id = None
            item.player_id = client.player
            item.save()

            get_item_message = self._get_item_message(
                client.player.name, item_meta.name
            )

            self.comms.send_to_vicinity(
                MessageRoute(get_item_message[0], client=client),
                MessageRoute(get_item_message[1], ids=[client.player.current_room_id]),
            )

        except (ClientNotLoggedIn, ItemNotFound):
            self.comms.send_prompt(client)

        except ActionMissingArguments:
            self.comms.send_to_client(
                MessageRoute(self._missing_args_message, client=client)
            )

        except RoomItemNotFound:
            self.comms.send_to_client(
                MessageRoute(self._room_item_not_found_message, client=client)
            )

        except ItemIsStationary:
            self.comms.send_to_client(
                MessageRoute(self._room_item_is_stationary_message, client=client)
            )
