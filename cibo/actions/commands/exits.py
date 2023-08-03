"""Returns the available exits."""

from typing import List, Optional

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import NotLoggedIn, RoomNotFound


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
                raise NotLoggedIn

            room = self.rooms.get_by_id(client.player.current_room_id)

        except (NotLoggedIn, RoomNotFound):
            self.send.prompt(client)

        else:
            self.send.private(client, self.rooms.get_formatted_exits(room))
