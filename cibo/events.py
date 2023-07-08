"""Events module"""

from cibo.output import Output
from cibo.telnet import TelnetServer

# TODO: think about using abstract classes for these


class Connect:
    """Contains logic for client connection events."""

    def __init__(self, telnet: TelnetServer, output: Output) -> None:
        self.telnet = telnet
        self.output = output

    def process(self) -> None:
        """Process new client connection events."""

        for new_client in self.telnet.get_new_clients():
            self.output.private(new_client, f"Welcome, you are client {new_client}.")


class Disconnect:
    """Contains logic for client disconnection events."""

    def __init__(self, telnet: TelnetServer, output: Output) -> None:
        self.telnet = telnet
        self.output = output

    def process(self) -> None:
        """Process client disconnection events."""

        for disconnected_client in self.telnet.get_disconnected_clients():
            for client in self.telnet.get_connected_clients():
                self.output.private(
                    client, f"Client {disconnected_client} disconnected."
                )


class Input:
    """Contains logic for incoming client input."""

    def __init__(self, telnet: TelnetServer, output: Output) -> None:
        self.telnet = telnet
        self.output = output

    def process(self) -> None:
        """Process incoming client input."""

        for sender_client, input_ in self.telnet.get_client_input():
            for client in self.telnet.get_connected_clients():
                self.output.private(client, f'{sender_client} says, "{input_}"')


class Events:
    """
    Event processor for the server. Kicks off the consumption and processing logic
    for each event type.
    """

    def __init__(self, telnet: TelnetServer, output: Output) -> None:
        self.telnet = telnet
        self.output = output

        self.connect = Connect(telnet=self.telnet, output=self.output)
        self.disconnect = Disconnect(telnet=self.telnet, output=self.output)
        self.input = Input(telnet=self.telnet, output=self.output)

    def process(self) -> None:
        """Processes any new server events, of all types."""

        self.connect.process()
        self.disconnect.process()
        self.input.process()
