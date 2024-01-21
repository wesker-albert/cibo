"""Events are server occurances of different types. Events can happen as a result of
client interactions with the server, or (in future) can be scheduled based upon a
tick timer or cron.

The EventInterface initializes events, so that they are available to receive signals.
"""

from cibo.actions.commands import ACTIONS
from cibo.actions.commands._processor_ import CommandProcessor
from cibo.events.connect import ConnectEvent
from cibo.events.disconnect import DisconnectEvent
from cibo.events.input import InputEvent
from cibo.events.spawn import SpawnEvent
from cibo.events.tick import TickEvent
from cibo.server_config import ServerConfig


class EventInterface:  # pytest: no cover
    """Event interface layer. Initializes events, so that they are available to
    receive signals.

    Args:
        server_config (ServerConfig): The server configuration object.
    """

    def __init__(self, server_config: ServerConfig) -> None:
        self._command_processor = CommandProcessor(server_config, ACTIONS)

        self._connect = ConnectEvent(server_config, "event-connect")
        self._disconnect = DisconnectEvent(server_config, "event-disconnect")
        self._input = InputEvent(server_config, "event-input", self._command_processor)
        self._tick = TickEvent(server_config, "event-tick")
        self._spawn = SpawnEvent(server_config, "event-spawn")
