"""Log out of the current player session."""

from time import sleep
from typing import List

from cibo.actions.__action__ import Action
from cibo.actions.connect import Connect
from cibo.client import Client


class Logout(Action):
    """Log out of the current player session."""

    def aliases(self) -> List[str]:
        return ["logout"]

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, command: str, args: List[str]) -> None:
        if not client.is_logged_in or not client.player:
            self.send.prompt(client)
            return

        player_name = client.player.name
        player_room = client.player.current_room_id

        client.log_out()

        self.send.local(
            player_room,
            "A black van pulls up, and 2 large men in labcoats abduct "
            f"[cyan]{player_name}[/]. The van speeds away. You wonder if "
            "you'll ever see your them again...",
            [client],
        )

        self.send.private(
            client,
            "You slowly fade away into obscurity, like you always feared you would...",
            prompt=False,
        )

        sleep(1)

        # process the connection Action, so the client knows they can now register
        # or login again
        Connect(self._telnet, self._world, self._output).process(client, command, args)
