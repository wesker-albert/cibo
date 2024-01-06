from cibo.models.message import Message, MessageRoute
from cibo.output.__output__ import Output


class Server(Output):
    def _format(self, message: Message) -> str:
        return f"\r{message}"

    def send(self, message: MessageRoute) -> None:
        for client in self._telnet.get_connected_clients():
            if (
                client.is_logged_in
                and client.player
                and client not in message.ignored_clients
            ):
                client.send_message(self._format(message.message))

                if message.send_prompt:
                    client.send_prompt()
