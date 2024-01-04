from typing import List

from cibo.client import Client
from cibo.messages.__message__ import Message
from cibo.messages.prompt import Prompt


class Private:
    def __init__(self) -> None:
        self._prompt = Prompt()

    def _format(self, message: Message) -> str:
        return f"\n{message}"

    def get(self, client: Client, message: Message, prompt: bool = True) -> List[str]:
        messages = [self._format(message)]

        if prompt:
            messages = messages + self._prompt.get(client)

        return messages

    def send(self, client: Client, message: Message, prompt: bool = True) -> None:
        """Prints a message intended for only one recipient."""

        client.send_message(self.get(client, message, prompt))
