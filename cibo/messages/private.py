from cibo.client import Client
from cibo.messages.__message__ import Message as MessageAbstract
from cibo.models.message import Message


class Private(MessageAbstract):
    def _format(self, message: Message) -> str:
        return f"\n{message}"

    def send(self, client: Client, message: Message, prompt: bool = True) -> None:
        """Prints a message intended for only one recipient."""

        client.send_message(self._format(message))

        if prompt:
            client.send_message(client.prompt)
