"""Returns information about the room or object targeted."""

from typing import List, Optional

from rich.panel import Panel

from cibo.actions.__action__ import Action
from cibo.actions.commands.exits import Exits
from cibo.client import Client


class Look(Action):
    """Returns information about the room or object targeted."""

    def aliases(self) -> List[str]:
        return ["l", "look"]

    def required_args(self) -> List[str]:
        return []

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
                occupant_client.player.current_room_id == client.player.current_room_id
                and occupant_client is not client
            )
        ]

        return "\n".join([str(occupant) for occupant in occupants])

    def process(self, client: Client, _command: Optional[str], args: List[str]):
        if not client.is_logged_in:
            self._send.prompt(client)
            return

        # the player is just looking at the room in general
        if not args:
            room = self.rooms.get_by_id(client.player.current_room_id)

            if room:
                exits = Exits(self._telnet, self._world).get_formatted_exits(client)

                occupants = self.get_formatted_occupants(client)
                # only include new lines if there are actual occupants
                occupants = f"\n\n{occupants}" if len(occupants) > 0 else ""

                self._send.private(
                    client,
                    Panel(
                        f"  {room.description.normal}{occupants}",
                        title=f"[blue]{room.name}[/]",
                        title_align="left",
                        subtitle=exits,
                        subtitle_align="right",
                        padding=(1, 4),
                    ),
                )

            return
