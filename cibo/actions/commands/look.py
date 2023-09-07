"""Returns information about the room or object targeted."""

from typing import List, Optional

from rich.panel import Panel

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import ClientNotLoggedIn, RoomNotFound
from cibo.models.data.item import Item
from cibo.models.data.npc import Npc
from cibo.models.room import Room


class Look(Action):
    """Returns information about the room or object targeted."""

    def aliases(self) -> List[str]:
        return ["l", "look"]

    def required_args(self) -> List[str]:
        return []

    def room_desc_message(self, room: Room, client: Client) -> Panel:
        """A stylized description of the room, including its exits and occupants."""

        items = self.get_formatted_items(client)
        occupants = self.get_formatted_occupants(client)

        if items or occupants:
            formatted_room_contents = f"\n\nLooking around you see:{items}{occupants}"
        else:
            formatted_room_contents = ""

        return Panel(
            f"  {room.description.normal}{formatted_room_contents}",
            title=f"[blue]{room.name}[/]",
            title_align="left",
            subtitle=room.get_formatted_exits(),
            subtitle_align="right",
            padding=(1, 4),
        )

    def _get_player_occupants(self, client: Client) -> List[str]:
        return [
            f"[cyan]{occupant_client.player.name}[/] is standing here."
            for occupant_client in self._telnet.get_connected_clients()
            if (
                occupant_client.player
                and client.player
                and occupant_client.player.current_room_id
                == client.player.current_room_id
                and occupant_client is not client
            )
        ]

    def _get_npc_occupants(self, client: Client) -> List[str]:
        return [
            self._world.npcs.get_by_id(npc.npc_id).room_description
            for npc in Npc.get_by_current_room_id(client.player.current_room_id)
        ]

    def _get_room_items(self, client: Client) -> List[str]:
        return [
            self.items.get_by_id(item.item_id).room_description
            for item in Item.get_by_current_room_id(client.player.current_room_id)
        ]

    def get_formatted_occupants(self, client: Client) -> str:
        """Formats and lists out all occupants of the Client's current room, sans the
        the Client themselves.

        Args:
            Client (Client): The client whose current room you want to get the
                occupants for.

        Returns:
            str: The occupants for the room.
        """

        player_occupants = self._get_player_occupants(client)
        npc_occupants = self._get_npc_occupants(client)
        combined_occupants = player_occupants + npc_occupants

        joined_occupants = "\n• ".join(
            [str(occupant) for occupant in combined_occupants]
        )

        # only include leading new lines if there are actual occupants
        return (
            f"\n• [bright_green]{joined_occupants}[/]"
            if len(combined_occupants) > 0
            else ""
        )

    def get_formatted_items(self, client: Client) -> str:
        """Formats and lists all the Items that are in the current room, and
        potentially interactable.

        Args:
            client (Client): The client whose current room you want to list the items
                from.

        Returns:
            str: The individual items the room contains.
        """

        room_items = self._get_room_items(client)

        joined_items = "\n• ".join([str(item) for item in room_items])

        return f"\n• [bright_blue]{joined_items}[/]" if len(room_items) > 0 else ""

    def process(self, client: Client, _command: Optional[str], args: List[str]) -> None:
        try:
            if not client.is_logged_in or args:
                raise ClientNotLoggedIn

            # the player is just looking at the room in general
            room = self.rooms.get_by_id(client.player.current_room_id)

        except (ClientNotLoggedIn, RoomNotFound):
            self.output.send_prompt(client)

        else:
            self.output.send_private_message(
                client, self.room_desc_message(room, client)
            )
