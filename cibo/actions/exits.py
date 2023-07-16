"""Returns the available exits."""

from typing import List, Optional

from cibo.actions import Action
from cibo.client import Client


class Exits(Action):
    """Returns the available exits."""

    def aliases(self) -> List[str]:
        return ["exits"]

    def required_args(self) -> List[str]:
        return []

    def get_formatted_exits(self, client: Client) -> Optional[str]:
        """Formats the exits into a pretty, stylized string.

        Args:
            client (Client): The Client to look up the room for.

        Returns:
            Optional[str]: The exits.
        """

        if not client.is_logged_in or not client.player:
            return None

        room = self._world.rooms.get(client.player.room)

        if room:
            exits = self._world.rooms.get_exits(client.player.room)

            # plurality is important...
            if not exits:
                return "[green]Exits:[/] none"

            if len(exits) == 1:
                return f"[green]Exit:[/] {exits[0]}"

            formatted_exits = ", ".join([str(exit_) for exit_ in exits])
            return f"[green]Exits:[/] {formatted_exits}"

        return None

    def process(self, client: Client, _command: Optional[str], _args: List[str]):
        if not client.is_logged_in or not client.player:
            self._send.prompt(client)
            return

        exits = self.get_formatted_exits(client)

        if not exits:
            self._send.prompt(client)
            return

        self._send.private(client, exits)
