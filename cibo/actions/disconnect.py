"""Make others aware that a player has abruptly disconnected."""

from typing import List, Optional

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.models.message import Message


class Disconnect(Action):
    """Make others aware that a player has abruptly disconnected."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(
        self, client: Client, _command: Optional[str], _args: List[str]
    ) -> None:
        if client.is_logged_in:
            client.player.save()

            self.output.send_room_message(
                client.player.current_room_id,
                Message(
                    f"You watch in horror as [cyan]{client.player.name}[/] "
                    "proceeds to slowly eat their own head. They eventually disappear "
                    "into nothingness."
                ),
                [client],
            )
