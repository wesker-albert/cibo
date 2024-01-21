"""Events are server occurances of different types. Events can happen as a result of
client interactions with the server, or (in future) can be scheduled based upon a
tick timer or cron.

The EventProcessor allows for the different event types to be processed as a batch,
in a FIFO order.
"""


from cibo.actions.commands import ACTIONS
from cibo.actions.commands._processor_ import CommandProcessor
from cibo.events.connect import ConnectEvent
from cibo.events.disconnect import DisconnectEvent
from cibo.events.input import InputEvent
from cibo.server_config import ServerConfig


class EventProcessor:  # pytest: no cover
    """Event processing abstraction layer for the server. Kicks off the processing
    logic for each included event type.

    Args:
        server_config (ServerConfig): The server configuration object.
    """

    def __init__(self, server_config: ServerConfig) -> None:
        self._command_processor = CommandProcessor(server_config, ACTIONS)

        self._connect = ConnectEvent(server_config, "event-connect")
        self._disconnect = DisconnectEvent(server_config, "event-disconnect")
        self._input = InputEvent(server_config, "event-input", self._command_processor)
