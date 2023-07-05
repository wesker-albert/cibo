# pylint: disable=too-few-public-methods
"""Events module"""

from cibo.telnet import TelnetServer


class Connect:
    """Contains logic for client connection events."""

    def process(self, telnet: TelnetServer, clients: list) -> None:
        """Process new client connection events."""

        for new_client in telnet.get_new_clients():
            # Add them to the client list
            clients.append(new_client)

            # Send a welcome message
            telnet.send_message(new_client, f"Welcome, you are client {new_client}.")


class Disconnect:
    """Contains logic for client disconnection events."""

    def process(self, telnet: TelnetServer, clients: list) -> None:
        """Process client disconnection events."""

        # For each client that has recently disconnected
        for disconnected_client in telnet.get_disconnected_clients():
            if disconnected_client not in clients:
                continue

            # Remove him from the clients list
            clients.remove(disconnected_client)

            # Send every client a message saying "Client X disconnected"
            for client in clients:
                telnet.send_message(
                    client, f"Client {disconnected_client} disconnected."
                )


class Message:
    """Contains logic for incoming client messages and input."""

    def process(self, telnet: TelnetServer, clients: list) -> None:
        """Process incoming client messages and input."""

        # For each message a client has sent
        for sender_client, message in telnet.get_messages():
            if sender_client not in clients:
                continue

            # Send every client a message reading:
            # "I received "[MESSAGE]" from client [ID OF THE SENDER CLIENT]"
            for client in clients:
                telnet.send_message(
                    client, f'I received "{message}" from client {sender_client}'
                )


class Events:
    """
    Event processor for the server. Kicks off the consumption and processing logic
    for each event type.
    """

    def __init__(self) -> None:
        self.connect = Connect()
        self.disconnect = Disconnect()
        self.message = Message()

    def process(self, telnet: TelnetServer, clients: list) -> None:
        """Processes any new server events, of all types."""

        self.connect.process(telnet, clients)
        self.disconnect.process(telnet, clients)
        self.message.process(telnet, clients)
