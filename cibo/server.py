"""Server module"""

import threading
from enum import Enum
from time import sleep

from peewee import SqliteDatabase

from cibo.events import Events
from cibo.models.player import Player
from cibo.telnet import TelnetServer


class Server:
    """
    A telnet server that once started, listens for incoming client events and messages.
    When an event is received, it determines the proper strategy interface then
    delegates the logic.
    """

    class Status(int, Enum):
        """Represents the current state of the server."""

        STOPPED = 1
        RUNNING = 2

    def __init__(self, port: int = 51234) -> None:
        """
        Creates a dormant telnet server. Once instantiated, it can be started and
        stopped.

        Args:
            port (int, optional): The port for telnet to listen on. Defaults to 51234.
        """

        self.telnet = TelnetServer(port=port)
        self.events = Events()
        self.database = SqliteDatabase("cibo_database.db")

        self.thread = None
        self.status = Server.Status.STOPPED
        self.clients = []

    @property
    def is_running(self) -> bool:
        """
        Check if the server is active and listening.

        Returns:
            bool: Is the server is running or not.
        """

        return self.status is Server.Status.RUNNING

    def __start_server(self) -> None:
        """Start the telnet server and begin listening for events."""

        self.telnet.listen()

        self.status = Server.Status.RUNNING

        while self.is_running:
            self.telnet.update()
            self.events.process(telnet=self.telnet, clients=self.clients)

            sleep(0.15)

    def create_db(self) -> None:
        """Create the sqlite DB and necessary tables."""

        self.database.connect()
        self.database.create_tables([Player])

    def start(self) -> None:
        """Create a thread and start the server."""

        self.thread = threading.Thread(target=self.__start_server)
        self.thread.start()

    def stop(self) -> None:
        """Stop the currently running server and end the thread."""

        self.status = Server.Status.STOPPED

        self.telnet.shutdown()
        self.thread.join()
