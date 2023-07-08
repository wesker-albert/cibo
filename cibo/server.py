"""Server module"""

import threading
from enum import Enum
from time import sleep
from typing import Optional

from peewee import SqliteDatabase

from cibo.events import Events
from cibo.messages import Messages
from cibo.models.player import Player
from cibo.output import Output
from cibo.telnet import TelnetServer


class Server:
    """
    A telnet server that once started, listens for incoming client events and input.
    When an event is received, it determines the proper strategy interface then
    delegates the logic.
    """

    class Status(int, Enum):
        """Represents the current state of the server."""

        STARTING_UP = 1
        RUNNING = 2
        SHUTTING_DOWN = 3
        STOPPED = 4

    def __init__(self, port: int = 51234) -> None:
        """
        Creates a dormant telnet server. Once instantiated, it can be started and
        stopped.

        Args:
            port (int, optional): The port for telnet to listen on. Defaults to 51234
        """

        self.telnet = TelnetServer(port=port)
        self.database = SqliteDatabase("cibo_database.db")
        self.messages = Messages("resources/output.json")
        self.output = Output(telnet=self.telnet, messages=self.messages)
        self.events = Events(telnet=self.telnet, output=self.output)

        self.thread: Optional[threading.Thread] = None
        self.status = Server.Status.STOPPED

    @property
    def is_running(self) -> bool:
        """
        Check if the server is active and listening.

        Returns:
            bool: Is the server is running or not
        """

        return self.status is Server.Status.RUNNING

    def __start_server(self) -> None:
        """Start the telnet server and begin listening for events."""

        self.status = Server.Status.STARTING_UP
        self.telnet.listen()
        self.status = Server.Status.RUNNING

        while self.is_running:
            self.telnet.update()
            self.events.process()

            sleep(0.15)

    def create_db(self) -> None:
        """Create the sqlite DB and necessary tables."""

        self.database.connect()
        self.database.create_tables([Player])

    def start(self) -> None:
        """Create a thread and start the server."""

        if self.status is Server.Status.STOPPED:
            self.thread = threading.Thread(target=self.__start_server)
            self.thread.start()

    def stop(self) -> None:
        """Stop the currently running server and end the thread."""

        if self.is_running and self.thread:
            self.status = Server.Status.SHUTTING_DOWN

            self.telnet.shutdown()
            self.thread.join()

            self.status = Server.Status.STOPPED
