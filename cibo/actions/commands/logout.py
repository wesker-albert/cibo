"""Log out of the current user session."""

from time import sleep
from typing import List, Tuple

from cibo.actions._base_ import Action
from cibo.actions.connect import Connect
from cibo.exceptions import ClientNotLoggedIn
from cibo.models.client import Client
from cibo.models.message import Message, MessageRoute


class Logout(Action):
    """Log out of the current user session."""

    def aliases(self) -> List[str]:
        return ["logout"]

    def required_args(self) -> List[str]:
        return []

    def _logging_out_message(self, user_name: str) -> Tuple[Message, Message]:
        """Successfully logging the user out."""

        return (
            Message(
                "You slowly fade away into obscurity, like you always feared you "
                "would..."
            ),
            Message(
                "A black van pulls up, and 2 large men in labcoats abduct "
                f"[cyan]{user_name}[/]. The van speeds away. You wonder if "
                "you'll ever see them again..."
            ),
        )

    def process(
        self, client: Client, command: str, args: List[str], sleep_time: int = 1
    ) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

        except ClientNotLoggedIn:
            self.comms.send_prompt(client)

        else:
            user_name = client.user.name
            user_room = client.user.current_room_id

            client.log_out()

            logging_out_message = self._logging_out_message(user_name)

            self.comms.send_to_vicinity(
                MessageRoute(logging_out_message[0], client=client, send_prompt=False),
                MessageRoute(logging_out_message[1], ids=[user_room]),
            )

            sleep(sleep_time)

            # process the connection action, so the client knows they can now register
            # or login again
            Connect(self._server_config).process(client, command, args)
