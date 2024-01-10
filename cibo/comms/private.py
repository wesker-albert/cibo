"""Sends a private message, to a specific client."""

from cibo.models import Message, MessageRoute
from cibo.comms._base_ import Comms


class Private(Comms):
    """Sends a private message, to a specific client."""

    def _format(self, message: Message) -> str:
        return f"\n{message}"

    def send(self, message: MessageRoute) -> None:
        if message.client:
            message.client.send_message(self._format(message.message))

            if message.send_prompt:
                message.client.send_prompt()
