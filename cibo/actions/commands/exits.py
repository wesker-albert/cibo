"""Returns the available exits."""

from typing import List, Optional

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import ClientNotLoggedIn, RoomNotFound
from cibo.messages.__message__ import Message


class Exits(Action):
    """Returns the available exits."""

    def aliases(self) -> List[str]:
        return ["exits"]

    def required_args(self) -> List[str]:
        return []

    def process(
        self, client: Client, _command: Optional[str], _args: List[str]
    ) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

            room = self.rooms.get_by_id(client.player.current_room_id)

        except (ClientNotLoggedIn, RoomNotFound):
            self.output.send_prompt(client)

        else:
            self.output.send_private_message(
                client, Message(room.get_formatted_exits())
            )
