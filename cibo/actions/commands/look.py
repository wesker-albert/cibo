"""Returns information about the room or object targeted."""

from typing import List, Optional

from rich.panel import Panel

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import ClientNotLoggedIn, RoomNotFound
from cibo.models.data.item import Item
from cibo.models.object.room import Room


class Look(Action):
    """Returns information about the room or object targeted."""

    def aliases(self) -> List[str]:
        return ["l", "look"]

    def required_args(self) -> List[str]:
        return []

    def room_desc_msg(self, room: Room, client: Client) -> Panel:
        """A stylized description of the room, including its exits and occupants."""

        return Panel(
            f"  {room.description.normal}"
            f"{self.get_formatted_occupants(client)}"
            f"{self.get_formatted_items(client)}",
            title=f"[blue]{room.name}[/]",
            title_align="left",
            subtitle=self.rooms.get_formatted_exits(room),
            subtitle_align="right",
            padding=(1, 4),
        )

    def get_formatted_occupants(self, client: Client) -> str:
        """Formats and lists out all occupants of the Client's current room, sans the
        the Client themselves.

        Args:
            Client (Client): The client whose current room you want to get the
                occupants for.

        Returns:
            str: The occupants for the room.
        """

        occupants = [
            f"[cyan]{occupant_client.player.name} is standing here.[/]"
            for occupant_client in self._telnet.get_connected_clients()
            if (
                occupant_client.player
                and client.player
                and occupant_client.player.current_room_id
                == client.player.current_room_id
                and occupant_client is not client
            )
        ]

        joined_occupants = "\n".join([str(occupant) for occupant in occupants])

        # only include leading new lines if there are actual occupants
        return f"\n\n{joined_occupants}" if len(occupants) > 0 else ""

    def get_formatted_items(self, client: Client) -> str:
        """Formats and lists all the Items that are in the current room, and
        potentially interactable.

        Args:
            client (Client): The client whose current room you want to list the items
                from.

        Returns:
            str: The individual items the room contains.
        """

        room_items = Item.get_by_room_id(client.player.current_room_id)

        inventory_items = [
            self.items.get_by_id(item.item_id).name for item in room_items
        ]

        inventory = "\n  ".join([str(item) for item in inventory_items])

        return (
            f"\n\n[yellow]You notice:[/]\n  {inventory}"
            if len(inventory_items) > 0
            else ""
        )

    def process(self, client: Client, _command: Optional[str], args: List[str]) -> None:
        try:
            if not client.is_logged_in or args:
                raise ClientNotLoggedIn

            # the player is just looking at the room in general
            room = self.rooms.get_by_id(client.player.current_room_id)

        except (ClientNotLoggedIn, RoomNotFound):
            self.send.prompt(client)

        else:
            self.send.private(client, self.room_desc_msg(room, client))
