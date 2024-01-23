"""Quits the game and disconnects the client."""

from time import sleep
from typing import List, Optional, Tuple

from cibo.actions import Action
from cibo.exceptions import ClientIsLoggedIn
from cibo.models.client import Client
from cibo.models.message import Message, MessageRoute


class Quit(Action):
    """Quits the game and disconnects the client."""

    @property
    def aliases(self) -> List[str]:
        return ["quit"]

    @property
    def required_args(self) -> List[str]:
        return []

    def _quitting_message(self, user_name: Optional[str]) -> Tuple[Message, Message]:
        """Successfully quitting the game."""

        return (
            Message(
                "You take the [blue]blue pill[/]. You wake up in your bed and believe "
                "whatever you want to believe. You choose to believe that your "
                "parents are proud of you.\n"
            ),
            Message(
                f'[cyan]{user_name}[/] yells, "Thank you Wisconsin!" They '
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
            user_name = client.user.name
            user_room = client.user.current_room_id

            client.log_out()

            self.comms.send_to_room(
                MessageRoute(
                    self._quitting_message(user_name)[1],
                    ids=[user_room],
                    ignored_clients=[client],
                )
            )

        finally:
            self.comms.send_to_client(
                MessageRoute(
                    self._quitting_message(None)[0], client=client, send_prompt=False
                )
            )

            sleep(sleep_time)
            client.disconnect()
