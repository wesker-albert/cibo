"""Events are server occurances of different types. Events can happen as a result of
client interactions with the server, or (in future) can be scheduled based upon a
tick timer or cron.

The EventProcessor allows for the different event types to be processed as a batch,
in a FIFO order.
"""

from cibo.actions.commands import ACTIONS
from cibo.actions.commands._processor_ import CommandProcessor
from cibo.events import ConnectEvent, DisconnectEvent, InputEvent
from cibo.server_config import ServerConfig


class EventProcessor:  # pytest: no cover
    """Event processing abstraction layer for the server. Kicks off the processing
    logic for each included event type.

    Args:
        server_config (ServerConfig): The server configuration object.
    """

    def __init__(self, server_config: ServerConfig) -> None:
        self._command_processor = CommandProcessor(server_config, ACTIONS)

        self._connect = ConnectEvent(server_config)
        self._disconnect = DisconnectEvent(server_config)
        self._input = InputEvent(server_config, self._command_processor)

    def process(self) -> None:
        """Processes the different event types."""

        self._connect.process()
        self._disconnect.process()
        self._input.process()
