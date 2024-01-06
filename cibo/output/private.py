from cibo.client import Client
from cibo.models.message import Message
from cibo.output.__output__ import Output


class Private(Output):
    def _format(self, message: Message) -> str:
        return f"\n{message}"

    def send(self, client: Client, message: Message, prompt: bool = True) -> None:
        """Prints a message intended for only one recipient."""

        client.send_message(self._format(message))

        if prompt:
            client.send_prompt()
