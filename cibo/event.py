"""Events occur when a client interacts with the server. The event processor allows for
the different Event types to be processed as a batch.
"""

from cibo.command import CommandProcessor
from cibo.events import Connect, Disconnect, Input
from cibo.telnet import TelnetServer


class EventProcessor:
    """Event processor abstraction layer for the server. Kicks off the consumption
    and processing logic for each Event type.
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
        """Processes any new server Events, of all types."""

        self._connect.process()
        self._disconnect.process()
        self._input.process()
