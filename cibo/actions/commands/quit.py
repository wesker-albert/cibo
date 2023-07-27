"""Quits the game and disconnects the client."""

from time import sleep
from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client


class Quit(Action):
    """Quits the game and disconnects the client."""

    def aliases(self) -> List[str]:
        return ["quit"]

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, _command: str, _args: List[str]) -> None:
        if client.is_logged_in and client.player:
            player_name = client.player.name
            player_room = client.player.current_room_id

            client.log_out()

            self.send.local(
                player_room,
                f'[cyan]{player_name}[/] yells, "Thank you Wisconsin!" They '
                "then proceed to drop their microphone, and walk off the stage.",
                [client],
            )

        self.send.private(
            client,
            "You take the [blue]blue pill[/]. You wake up in your bed and believe "
            "whatever you want to believe. You choose to believe that your parents are "
            "proud of you.\n",
            prompt=False,
        )

        sleep(1)

        client.disconnect()
