"""Instantiates a telnet server, and then supplies event processing for the server, as
well as methods to control the server state.
"""

import os
import threading
from enum import Enum
from time import sleep
from typing import Optional

from peewee import SqliteDatabase

from cibo.decorator import load_environment_variables
from cibo.event import EventProcessor
from cibo.models.player import Player
from cibo.telnet import TelnetServer


class Server:
    """A telnet server that once started, listens for incoming client events and input.
    When a new event is received upon update, it calls upon the event processor to
    determine event type and then carry out the event logic.
    """

    class Status(int, Enum):
        """Represents the current state of the server."""

        STARTING_UP = 1
        RUNNING = 2
        SHUTTING_DOWN = 3
        STOPPED = 4

    @load_environment_variables
    def __init__(self, port: Optional[int] = None) -> None:
        """Creates a dormant telnet server. Once instantiated, it can be started and
        stopped.

        Args:
            port (int, optional): The port for telnet to listen on. Defaults to 51234
        """

        self.database = SqliteDatabase(os.getenv("DATABASE_PATH", "cibo_database.db"))

        self._port = port or int(os.getenv("SERVER_PORT", "51234"))
        self._telnet = TelnetServer(port=self._port)
        self._event_processor = EventProcessor(self._telnet)

        self._thread: Optional[threading.Thread] = None
        self._status = self.Status.STOPPED

    @property
    def is_running(self) -> bool:
        """Check if the server is active and listening.

        Returns:
            bool: Is the server is running or not
        """

        return self._status is self.Status.RUNNING

    def _start_server(self) -> None:
        """Start the telnet server and begin listening for events. Process any new
        events received using the event processor.
        """

        self._status = self.Status.STARTING_UP
        self._telnet.listen()
        self._status = self.Status.RUNNING

        while self.is_running:
            self._telnet.update()
            self._event_processor.process()

            sleep(0.15)

    def create_db(self) -> None:
        """Create the sqlite DB and necessary tables."""

        self.database.connect()
        self.database.create_tables([Player])

    def start(self) -> None:
        """Create a thread and start the server."""

        if self._status is self.Status.STOPPED:
            self._thread = threading.Thread(target=self._start_server)
            self._thread.start()

    def stop(self) -> None:
        """Stop the currently running server and end the thread."""

        if self.is_running and self._thread:
            self._status = self.Status.SHUTTING_DOWN

            self._telnet.shutdown()
            self._thread.join()

            self._status = self.Status.STOPPED
