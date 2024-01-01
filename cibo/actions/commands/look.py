"""Returns information about the room or object targeted."""

from typing import List, Optional

from rich.panel import Panel

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import ActionMissingArguments, ClientNotLoggedIn
from cibo.models.data.item import Item as ItemData
from cibo.models.data.npc import Npc as NpcData
from cibo.models.item import Item
from cibo.models.npc import Npc
from cibo.models.room import Room


class Look(Action):
    """Returns information about the room or object targeted."""

    def aliases(self) -> List[str]:
        return ["l", "look"]

    def required_args(self) -> List[str]:
        return []

    def room_desc_message(self, client: Client, room: Room) -> Panel:
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

    def resource_desc_message(self, client: Client, args: List[str]) -> str:
        """A stylized description of an item in the room, an item in the player's
        inventory, or an NPC in the room. In that order.
        """

        resource = self.items.get_by_name(
            (
                self._get_room_items(client)
                + self._get_player_items(client)
                + self._get_npc_occupants(client)
            ),
            args[0],
        )

        if resource:
            return f"You look at {resource.name}:\n\n  {resource.description.look}"

        return "You don't see that..."

    def _get_player_occupants(self, client: Client) -> List[Client]:
        return [
            occupant_client
            for occupant_client in self._telnet.get_connected_clients()
            if (
                occupant_client.player
                and client.player
                and occupant_client.player.current_room_id
                == client.player.current_room_id
                and occupant_client is not client
            )
        ]

    def _get_npc_occupants(self, client: Client) -> List[Npc]:
        return self.npcs.get_from_dataset(
            NpcData.get_by_current_room_id(client.player.current_room_id)
        )

    def _get_room_items(self, client: Client) -> List[Item]:
        return self.items.get_from_dataset(
            ItemData.get_by_current_room_id(client.player.current_room_id)
        )

    def _get_player_items(self, client: Client) -> List[Item]:
        return self.items.get_from_dataset(client.player.inventory)

    def get_formatted_occupants(self, client: Client) -> str:
        """Formats and lists out all occupants of the client's current room, excluding
        the client themself.

        Args:
            Client (Client): The client whose current room you want to get the
                occupants for.

        Returns:
            str: The occupants for the room.
        """

        player_occupants = [
            f"[cyan]{occupant_client.player.name}[/] is standing here."
            for occupant_client in self._get_player_occupants(client)
        ]
        npc_occupants = [
            npc.room_description for npc in self._get_npc_occupants(client)
        ]
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
        """Formats and lists all the items that are in the current room, and
        potentially interactable.

        Args:
            client (Client): The client whose current room you want to list the items
                from.

        Returns:
            str: The individual items the room contains.
        """

        room_items = [item.room_description for item in self._get_room_items(client)]

        joined_items = "\n• ".join([str(item) for item in room_items])

        return f"\n• [bright_blue]{joined_items}[/]" if len(room_items) > 0 else ""

    def process(self, client: Client, _command: Optional[str], args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

            if not args:
                raise ActionMissingArguments

            self.output.send_private_message(
                client, self.resource_desc_message(client, args)
            )

        except ClientNotLoggedIn:
            self.output.send_prompt(client)

        except ActionMissingArguments:
            # the player is just looking at the room in general
            room = self.rooms.get_by_id(client.player.current_room_id)

            self.output.send_private_message(
                client, self.room_desc_message(client, room)
            )
