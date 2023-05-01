import threading
from enum import Enum
from time import sleep

from cibo.telnet import TelnetServer


class ServerStatus(int, Enum):
    """Represents the current state of the server"""

    STOPPED = 1
    RUNNING = 2


class Server:
    """Creates a telnet server isntance that can listen for and respond to events"""

    def __init__(self, port: int = 51234) -> None:
        self.telnet = TelnetServer(port=port)
        self.thread = None
        self.status = ServerStatus.STOPPED
        self.clients = []

    @property
    def is_running(self) -> bool:
        """Check if the server is active and listening

        Returns:
            bool: is the server is running or not
        """
        return self.status is ServerStatus.RUNNING

    def __process_connect_event(self) -> None:
        """Consume new client connection events"""

        for new_client in self.telnet.get_new_clients():
            # Add them to the client list
            self.clients.append(new_client)

            # Send a welcome message
            self.telnet.send_message(
                new_client, f"Welcome, you are client {new_client}."
            )

    def __process_disconnect_event(self) -> None:
        """Consume client disconnection events"""

        # For each client that has recently disconnected
        for disconnected_client in self.telnet.get_disconnected_clients():
            if disconnected_client not in self.clients:
                continue

            # Remove him from the clients list
            self.clients.remove(disconnected_client)

            # Send every client a message saying "Client X disconnected"
            for client in self.clients:
                self.telnet.send_message(
                    client, f"Client {disconnected_client} disconnected."
                )

    def __process_message_event(self) -> None:
        """Consume incoming client messages and input"""

        # For each message a client has sent
        for sender_client, message in self.telnet.get_messages():
            if sender_client not in self.clients:
                continue

            # Send every client a message reading:
            # "I received "[MESSAGE]" from client [ID OF THE SENDER CLIENT]"
            for client in self.clients:
                self.telnet.send_message(
                    client, f'I received "{message}" from client {sender_client}'
                )

    def __start_server(self) -> None:
        self.telnet.listen()

        self.status = ServerStatus.RUNNING

        while self.status is ServerStatus.RUNNING:
            self.telnet.update()

            self.__process_connect_event()
            self.__process_disconnect_event()
            self.__process_message_event()

            sleep(0.15)

    def start(self) -> None:
        """Create a thread and start the server"""

        self.thread = threading.Thread(target=self.__start_server)
        self.thread.start()

    def stop(self) -> None:
        """Stop the currently running server and end the thread"""
        self.status = ServerStatus.STOPPED

        self.telnet.shutdown()
        self.thread.join()


if __name__ == "__main__":
    # This block of code is intended as temporary, while the meat and potatoes of the
    # server is being developed. TODO: instead use a daemonization approach where
    # the server is started and stopped from the commandline, and not while a loop is
    # running

    server = Server()

    print(
        "Accepted commands:\n\n"
        "start    start the server\n"
        "stop     stop the server\n"
        "exit     stop the server if running, and exit this program\n"
    )

    while True:
        user_input = input("> ").lower()

        if user_input == "start":
            if not server.is_running:
                server.start()

                print("Started server.")

                continue

            if server.is_running:
                print("Server is already running.")

        if user_input == "stop":
            if server.is_running:
                server.stop()
                print("Stopped server.")

                continue

            if not server.is_running:
                print("Server is not running.")

        if user_input == "exit":
            if server.is_running:
                server.stop()
                print("Stopped server.")

            print("Goodbye!")
            break

        sleep(1)
