"""Make others aware that a player has abruptly disconnected."""

from typing import List, Optional

from cibo.actions.__action__ import Action
from cibo.models import Client, Message, MessageRoute


class Disconnect(Action):
    """Make others aware that a player has abruptly disconnected."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def _disconnect_message(self, player_name: str) -> Message:
        return Message(
            f"You watch in horror as [cyan]{player_name}[/] proceeds to slowly eat "
            "their own head. They eventually disappear into nothingness."
        )

    def process(
        self, client: Client, _command: Optional[str], _args: List[str]
    ) -> None:
        if client.is_logged_in:
            client.player.save()

            self.output.send_to_room(
                MessageRoute(
                    self._disconnect_message(client.player.name),
                    ids=[client.player.current_room_id],
                    ignored_clients=[client],
                )
            )
