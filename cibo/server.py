import threading
from enum import Enum

from cibo.telnet import TelnetServer


class ServerStatus(int, Enum):
    STOPPED = 1
    RUNNING = 2


class Server:
    def __init__(self, port: int = 51234) -> None:
        self.server = TelnetServer(port=port)
        self.status = ServerStatus.STOPPED
        self.clients = []

    @property
    def is_running(self) -> bool:
        return self.status is ServerStatus.RUNNING

    def start(self) -> None:
        self.status = ServerStatus.RUNNING

        while self.status is ServerStatus.RUNNING:
            # Make the server parse all the new events
            self.server.update()

            # For each newly connected client
            for new_client in self.server.get_new_clients():
                # Add them to the client list
                self.clients.append(new_client)

                # Send a welcome message
                self.server.send_message(
                    new_client, f"Welcome, you are client {new_client}."
                )

            # For each client that has recently disconnected
            for disconnected_client in self.server.get_disconnected_clients():
                if disconnected_client not in self.clients:
                    continue

                # Remove him from the clients list
                self.clients.remove(disconnected_client)

                # Send every client a message saying "Client X disconnected"
                for client in self.clients:
                    self.server.send_message(
                        client, f"Client {disconnected_client} disconnected."
                    )

            # For each message a client has sent
            for sender_client, message in self.server.get_messages():
                if sender_client not in self.clients:
                    continue

                # Send every client a message reading:
                # "I received "[MESSAGE]" from client [ID OF THE SENDER CLIENT]"
                for client in self.clients:
                    self.server.send_message(
                        client, f'I received "{message}" from client {sender_client}'
                    )

    def stop(self) -> None:
        self.status = ServerStatus.STOPPED
        self.server.shutdown()


if __name__ == "__main__":
    server = Server()

    while True:
        user_input = input().lower()

        if user_input == "start":
            if not server.is_running:
                server_thread = threading.Thread(target=server.start)
                server_thread.start()

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
