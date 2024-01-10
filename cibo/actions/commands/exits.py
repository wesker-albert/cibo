"""Returns the available exits."""

from typing import List, Optional

from cibo.actions._base_ import Action
from cibo.exceptions import ClientNotLoggedIn, RoomNotFound
from cibo.models.client import Client
from cibo.models.message import Message, MessageRoute
from cibo.models.room import Room


class Exits(Action):
    """Returns the available exits."""

    def aliases(self) -> List[str]:
        return ["exits"]

    def required_args(self) -> List[str]:
        return []

    def _exits_message(self, room: Room) -> Message:
        """The exits for the current room."""

        return Message(room.get_formatted_exits())

    def process(
        self, client: Client, _command: Optional[str], _args: List[str]
    ) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

            room = self.rooms.get_by_id(client.player.current_room_id)

        except (ClientNotLoggedIn, RoomNotFound):
            self.comms.send_prompt(client)

        else:
            self.comms.send_to_client(
                MessageRoute(self._exits_message(room), client=client)
            )
