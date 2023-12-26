"""Events are server occurances of different types. Events can happen as a result of
client interactions with the server, or (in future) can be scheduled based upon a
tick timer or cron.

The EventProcessor allows for the different Event types to be processed as a batch,
in a FIFO order.
"""

from cibo.actions.commands import ACTIONS
from cibo.command import CommandProcessor
from cibo.config import ServerConfig
from cibo.events.connect import ConnectEvent
from cibo.events.disconnect import DisconnectEvent
from cibo.events.input import InputEvent


class EventProcessor:  # pytest: no cover
    """Event processing abstraction layer for the server. Kicks off the processing
    logic for each included Event type.
    """

    def __init__(self, server_config: ServerConfig) -> None:
        """Creates the Event processor instance.

        Args:
            telnet (TelnetServer): The Telnet server to use for event query and
                processing.
            world (World): The world, and all its resources.
        """

        self._telnet = server_config.telnet
        self._world = server_config.world
        self._output = server_config.output

        self._command_processor = CommandProcessor(server_config, ACTIONS)

        self._connect = ConnectEvent(server_config)
        self._disconnect = DisconnectEvent(server_config)
        self._input = InputEvent(server_config, self._command_processor)

    def process(self) -> None:
        """Processes the different Event types."""

        self._connect.process()
        self._disconnect.process()
        self._input.process()
