"""Returns information about the room or object targeted."""

from typing import List, Optional, Union

from rich.panel import Panel

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import ActionMissingArguments, ClientNotLoggedIn, ResourceNotFound
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

    def _get_player_occupants_descriptions(self, client: Client) -> List[str]:
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

    def _get_npc_occupants(self, client: Client) -> List[Npc]:
        return [
            self._world.npcs.get_by_id(npc.npc_id)
            for npc in NpcData.get_by_current_room_id(client.player.current_room_id)
        ]

    def _get_npc_occupants_descriptions(self, client: Client) -> List[str]:
        return [npc.room_description for npc in self._get_npc_occupants(client)]

    def _get_room_items(self, client: Client) -> List[Item]:
        return [
            self.items.get_by_id(item.item_id)
            for item in ItemData.get_by_current_room_id(client.player.current_room_id)
        ]

    def _get_room_items_descriptions(self, client: Client) -> List[str]:
        return [item.room_description for item in self._get_room_items(client)]

    def _get_resource_look_description_by_name(
        self, resources: Union[List[Item], List[Npc]], name: str
    ) -> Optional[str]:
        search_name = name
        name_segments = name.split(".")

        if name_segments[0].isdigit():
            search_name = name_segments[1]

        results = [
            resource.description.look
            for resource in resources
            if search_name in resource.name
        ]

        if not results:
            return None

        if name_segments[0].isdigit():
            try:
                return results[int(name_segments[0])]

            except IndexError:
                return None

        return results[0]

    def get_formatted_occupants(self, client: Client) -> str:
        """Formats and lists out all occupants of the client's current room, excluding
        the client themself.

        Args:
            Client (Client): The client whose current room you want to get the
                occupants for.

        Returns:
            str: The occupants for the room.
        """

        player_occupants = self._get_player_occupants_descriptions(client)
        npc_occupants = self._get_npc_occupants_descriptions(client)
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

        room_items = self._get_room_items_descriptions(client)

        joined_items = "\n• ".join([str(item) for item in room_items])

        return f"\n• [bright_blue]{joined_items}[/]" if len(room_items) > 0 else ""

    def process(self, client: Client, _command: Optional[str], args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

            if not args:
                raise ActionMissingArguments

            room_item = self._get_resource_look_description_by_name(
                self._get_room_items(client), args[0]
            )
            npc_occupant = self._get_resource_look_description_by_name(
                self._get_npc_occupants(client), args[0]
            )

            if room_item:
                self.output.send_private_message(client, room_item)
            elif npc_occupant:
                self.output.send_private_message(client, npc_occupant)
            else:
                raise ResourceNotFound

        except ClientNotLoggedIn:
            self.output.send_prompt(client)

        except ResourceNotFound:
            self.output.send_private_message(client, "You don't see that.")

        except ActionMissingArguments:
            # the player is just looking at the room in general
            room = self.rooms.get_by_id(client.player.current_room_id)

            self.output.send_private_message(
                client, self.room_desc_message(room, client)
            )
