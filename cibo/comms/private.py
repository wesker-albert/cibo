"""Sends a private message, to a specific client."""


from cibo.comms import Comm
from cibo.models.message import Message, MessageRoute


class Private(Comm):
    """Sends a private message, to a specific client."""

    def _format(self, message: Message) -> str:
        return f"\n{message}"

    def send(self, message: MessageRoute) -> None:
        if message.client:
            message.client.send_message(self._format(message.message))

            if message.send_prompt:
                message.client.send_prompt()
