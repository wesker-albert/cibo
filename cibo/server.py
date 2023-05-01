"""Server module"""

import threading
from enum import Enum
from time import sleep

from cibo.events import Events
from cibo.telnet import TelnetServer


class ServerStatus(int, Enum):
    """Represents the current state of the server."""

    STOPPED = 1
    RUNNING = 2


class Server:
    """
    A telnet server that once started, listens for incoming client events and messages.
    When an event is received, it determines the proper strategy interface then
    delegates the logic.
    """

    def __init__(self, port: int = 51234) -> None:
        """
        Creates a dormant telnet server. Once instantiated, it can be started and
        stopped.

        Args:
            port (int, optional): The port for telnet to listen on. Defaults to 51234.
        """

        self.telnet = TelnetServer(port=port)
        self.events = Events()

        self.thread = None
        self.status = ServerStatus.STOPPED
        self.clients = []

    @property
    def is_running(self) -> bool:
        """
        Check if the server is active and listening.

        Returns:
            bool: Is the server is running or not.
        """

        return self.status is ServerStatus.RUNNING

    def __start_server(self) -> None:
        """Start the telnet server and begin listening for events."""

        self.telnet.listen()

        self.status = ServerStatus.RUNNING

        while self.status is ServerStatus.RUNNING:
            self.telnet.update()
            self.events.process(telnet=self.telnet, clients=self.clients)

            sleep(0.15)

    def start(self) -> None:
        """Create a thread and start the server."""

        self.thread = threading.Thread(target=self.__start_server)
        self.thread.start()

    def stop(self) -> None:
        """Stop the currently running server and end the thread."""

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
