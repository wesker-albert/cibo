"""Events are server occurances of different types. Events can happen as a result of
client interactions with the server, or (in future) can be scheduled based upon a
tick timer or cron.

The EventProcessor allows for the different Event types to be processed as a batch,
in a FIFO order.
"""

from cibo.events.connect import ConnectEvent
from cibo.events.disconnect import DisconnectEvent
from cibo.events.input import InputEvent
from cibo.output import Output
from cibo.resources.world import World
from cibo.telnet import TelnetServer


class EventProcessor:  # pytest: no cover
    """Event processing abstraction layer for the server. Kicks off the processing
    logic for each included Event type.
    """

    def __init__(self, telnet: TelnetServer, world: World, output: Output) -> None:
        """Creates the Event processor instance.

        Args:
            telnet (TelnetServer): The Telnet server to use for event query and
                processing.
            world (World): The world, and all its resources.
        """

        self._telnet = telnet
        self._world = world
        self._output = output

        self._connect = ConnectEvent(self._telnet, self._world, self._output)
        self._disconnect = DisconnectEvent(self._telnet, self._world, self._output)
        self._input = InputEvent(self._telnet, self._world, self._output)

    def process(self) -> None:
        """Processes the different Event types."""

        self._connect.process()
        self._disconnect.process()
        self._input.process()
