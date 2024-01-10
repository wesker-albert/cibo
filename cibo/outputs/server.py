"""Sends a server-wide message to clients who are currently logged into a
player session.
"""

from cibo.models import Message, MessageRoute
from cibo.outputs.__output__ import Output


class Server(Output):
    """Sends a server-wide message to clients who are currently logged into a
    player session.
    """

    def _format(self, message: Message) -> str:
        return f"\r{message}"

    def send(self, message: MessageRoute) -> None:
        for client in self._telnet.get_connected_clients():
            if client.is_logged_in and client not in message.ignored_clients:
                client.send_message(self._format(message.message))

                if message.send_prompt:
                    client.send_prompt()