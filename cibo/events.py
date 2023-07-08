"""Events module"""

from cibo.output import Output
from cibo.telnet import TelnetServer

# TODO: think about using abstract classes for these


class Connect:
    """Contains logic for client connection events."""

    def __init__(self, output: Output) -> None:
        self.output = output

    def process(self, telnet: TelnetServer, clients: list) -> None:
        """Process new client connection events."""

        for new_client in telnet.get_new_clients():
            # Add them to the client list
            clients.append(new_client)

            # Send a welcome message
            self.output.private(
                new_client,
                f"Welcome, you are client {new_client}.",
            )


class Disconnect:
    """Contains logic for client disconnection events."""

    def __init__(self, output: Output) -> None:
        self.output = output

    def process(self, telnet: TelnetServer, clients: list) -> None:
        """Process client disconnection events."""

        # For each client that has recently disconnected
        for disconnected_client in telnet.get_disconnected_clients():
            if disconnected_client not in clients:
                continue

            # Remove them from the clients list
            clients.remove(disconnected_client)

            # Send every client a message saying "Client X disconnected"
            for client in clients:
                self.output.private(
                    client, f"Client {disconnected_client} disconnected."
                )


class Input:
    """Contains logic for incoming client input."""

    def __init__(self, output: Output) -> None:
        self.output = output

    def process(self, telnet: TelnetServer, clients: list) -> None:
        """Process incoming client input."""

        # For each input message a client has sent
        for sender_client, input_ in telnet.get_client_input():
            if sender_client not in clients:
                continue

            # Send every client the message.
            for client in clients:
                self.output.private(client, f'{sender_client} says, "{input_}"')


class Events:
    """
    Event processor for the server. Kicks off the consumption and processing logic
    for each event type.
    """

    def __init__(self, output: Output) -> None:
        self.output = output

        self.connect = Connect(output=self.output)
        self.disconnect = Disconnect(output=self.output)
        self.input = Input(output=self.output)

    def process(self, telnet: TelnetServer, clients: list) -> None:
        """Processes any new server events, of all types."""

        self.connect.process(telnet, clients)
        self.disconnect.process(telnet, clients)
        self.input.process(telnet, clients)
