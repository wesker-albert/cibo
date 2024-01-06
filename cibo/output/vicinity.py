from typing import Optional

from cibo.models.message import MessageRoute
from cibo.output.__output__ import OutputChain


# pylint: disable=arguments-differ
class Vicinity(OutputChain):
    def send(
        self,
        client_message: MessageRoute,
        room_message: MessageRoute,
        vicinity_message: Optional[MessageRoute] = None,
    ) -> None:
        if client_message.client:
            self._private.send(client_message)

            room_message.ignored_clients = [client_message.client]
            self._room.send(room_message)

            if vicinity_message:
                vicinity_message.ignored_clients = [client_message.client]
                self._room.send(vicinity_message)
