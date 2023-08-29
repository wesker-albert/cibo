"""Quits the game and disconnects the client."""

from time import sleep
from typing import List, Optional

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import ClientIsLoggedIn
from cibo.output import Announcement


class Quit(Action):
    """Quits the game and disconnects the client."""

    def aliases(self) -> List[str]:
        return ["quit"]

    def required_args(self) -> List[str]:
        return []

    def quitting_message(self, player_name: Optional[str]) -> Announcement:
        """Successfully quitting the game."""

        return Announcement(
            "You take the [blue]blue pill[/]. You wake up in your bed and believe "
            "whatever you want to believe. You choose to believe that your parents are "
            "proud of you.\n",
            f'[cyan]{player_name}[/] yells, "Thank you Wisconsin!" They '
            "then proceed to drop their microphone, and walk off the stage.",
        )

    def process(self, client: Client, _command: str, _args: List[str]) -> None:
        try:
            if client.is_logged_in:
                raise ClientIsLoggedIn

        except ClientIsLoggedIn:
            player_name = client.player.name
            player_room = client.player.current_room_id

            client.log_out()

            self.output.send_local_message(
                player_room, self.quitting_message(player_name).room_message, [client]
            )

        finally:
            self.output.send_private_message(
                client, self.quitting_message(None).self_message, prompt=False
            )

            sleep(1)
            client.disconnect()
