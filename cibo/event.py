"""Events are server occurances of different types. Events can happen as a result of
client interactions with the server, or (in future) can be scheduled based upon a
tick timer or cron.

The EventProcessor allows for the different Event types to be processed as a batch.
"""

from cibo.command import CommandProcessor
from cibo.events import Connect, Disconnect, Input
from cibo.telnet import TelnetServer


class EventProcessor:
    """Event processing abstraction layer for the server. Kicks off the processing
    logic for each included Event type.
    """

    def __init__(
        self, telnet: TelnetServer, command_processor: CommandProcessor
    ) -> None:
        """Creates the Event processor instance.

        Args:
            telnet (TelnetServer): The Telnet server to use for event query and
                processing
            command_processor (CommandProcessor): The CommandProcessor used for
                processing client input
        """

        self._telnet = telnet
        self._command_processor = command_processor

        self._connect = Connect(self._telnet)
        self._disconnect = Disconnect(self._telnet)
        self._input = Input(self._telnet, self._command_processor)

    def process(self) -> None:
        """Processes the different Event types."""

        self._connect.process()
        self._disconnect.process()
        self._input.process()
