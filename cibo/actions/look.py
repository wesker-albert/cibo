"""Returns information about the room or object targeted."""

from typing import List, Optional

from rich.panel import Panel

from cibo.actions import Action
from cibo.actions.exits import Exits
from cibo.client import Client


class Look(Action):
    """Returns information about the room or object targeted."""

    def aliases(self) -> List[str]:
        return ["l", "look"]

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, _command: Optional[str], args: List[str]):
        if not client.is_logged_in or not client.player:
            self._send.prompt(client)
            return

        # the player is just looking at the room in general
        if not args:
            room = self._world.rooms.get(client.player.room)

            if room:
                exits = Exits(self._telnet, self._world).get_formatted_exits(client)

                self._send.private(
                    client,
                    Panel(
                        f"  {room.description.normal}",
                        title=f"[blue]{room.name}[/]",
                        title_align="left",
                        subtitle=exits,
                        subtitle_align="right",
                        padding=(1, 4),
                    ),
                )

            return
