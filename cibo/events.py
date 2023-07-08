"""Events module"""

from abc import ABC, abstractmethod

from cibo.output import Output
from cibo.telnet import TelnetServer


class Event(ABC):
    """The base interface used by other event classes."""

    def __init__(self, telnet: TelnetServer) -> None:
        self.telnet = telnet
        self.output = Output(self.telnet)

    @abstractmethod
    def process(self) -> None:
        """Abstract method for event processing."""

        pass  # pylint: disable=unnecessary-pass

class EventProcessor(Event):
    """Event processor for the server. Kicks off the consumption and processing logic
    for each event type.
    """

    def __init__(self, telnet: TelnetServer) -> None:
        """Creates the event processor instance, used to kick off the processing logic
        for each of the different event types we expect.

        Args:
            telnet (TelnetServer): The Telnet server to use for event query and
                processing
        """

        super().__init__(telnet)

        self._connect = Connect(self.telnet)
        self._disconnect = Disconnect(self.telnet)
        self._input = Input(self.telnet)

    def process(self) -> None:
        """Processes any new server events, of all types."""

        self._connect.process()
        self._disconnect.process()
        self._input.process()


class Connect(Event):
    """Contains logic for client connection events."""

    def process(self) -> None:
        """Process new client connection events."""

        for new_client in self.telnet.get_new_clients():
            self.output.private(new_client, f"Welcome, you are client {new_client}.")


class Disconnect(Event):
    """Contains logic for client disconnection events."""

    def process(self) -> None:
        """Process client disconnection events."""

        for disconnected_client in self.telnet.get_disconnected_clients():
            for client in self.telnet.get_connected_clients():
                self.output.private(
                    client, f"Client {disconnected_client} disconnected."
                )


class Input(Event):
    """Contains logic for incoming client input."""

    def process(self) -> None:
        """Process incoming client input."""

        for sender_client, input_ in self.telnet.get_client_input():
            for client in self.telnet.get_connected_clients():
                self.output.private(client, f'{sender_client} says, "{input_}"')
