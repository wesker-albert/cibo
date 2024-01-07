"""Sends a private message, to a specific client."""

from cibo.models.message import Message, MessageRoute
from cibo.outputs.__output__ import Output


class Private(Output):
    """Sends a private message, to a specific client."""

    def _format(self, message: Message) -> str:
        return f"\n{message}"

    def send(self, message: MessageRoute) -> None:
        """Prints a message intended for only one recipient."""
        if message.client:
            message.client.send_message(self._format(message.message))

            if message.send_prompt:
                message.client.send_prompt()
