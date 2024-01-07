"""Quits the game and disconnects the client."""

from time import sleep
from typing import List, Optional, Tuple

from cibo.actions.__action__ import Action
from cibo.exception import ClientIsLoggedIn
from cibo.models.client import Client
from cibo.models.message import Message, MessageRoute


class Quit(Action):
    """Quits the game and disconnects the client."""

    def aliases(self) -> List[str]:
        return ["quit"]

    def required_args(self) -> List[str]:
        return []

    def _quitting_message(self, player_name: Optional[str]) -> Tuple[Message, Message]:
        """Successfully quitting the game."""

        return (
            Message(
                "You take the [blue]blue pill[/]. You wake up in your bed and believe "
                "whatever you want to believe. You choose to believe that your "
                "parents are proud of you.\n"
            ),
            Message(
                f'[cyan]{player_name}[/] yells, "Thank you Wisconsin!" They '
                "then proceed to drop their microphone, and walk off the stage."
            ),
        )

    def process(
        self, client: Client, _command: str, _args: List[str], sleep_time: int = 1
    ) -> None:
        try:
            if client.is_logged_in:
                raise ClientIsLoggedIn

        except ClientIsLoggedIn:
            player_name = client.player.name
            player_room = client.player.current_room_id

            client.log_out()

            self.output.send_to_room(
                MessageRoute(
                    self._quitting_message(player_name)[1],
                    ids=[player_room],
                    ignored_clients=[client],
                )
            )

        finally:
            self.output.send_to_client(
                MessageRoute(
                    self._quitting_message(None)[0], client=client, send_prompt=False
                )
            )

            sleep(sleep_time)
            client.disconnect()
