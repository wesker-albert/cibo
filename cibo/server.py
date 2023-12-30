"""Instantiates a telnet server. Provides event processing for the telnet server, as
well as methods to control the server state.
"""

from enum import Enum
from os import getenv
from threading import Thread
from time import sleep

from peewee import SqliteDatabase

from cibo.config import ServerConfig
from cibo.event import EventProcessor
from cibo.events.spawn import SpawnEvent
from cibo.events.tick import TickEvent
from cibo.models.data.item import Item
from cibo.models.data.npc import Npc
from cibo.models.data.player import Player


class Server:
    """A telnet server that once started, listens for incoming client events and input.
    When a new event is received upon update, it calls upon the event processor to
    determine event type and then carry out the event logic.

    Args:
        server_config (ServerConfig): The server configuration object.
    """

    class Status(int, Enum):
        """Represents the current state of the server."""

        STARTING_UP = 1
        RUNNING = 2
        SHUTTING_DOWN = 3
        STOPPED = 4

    def __init__(self, server_config: ServerConfig) -> None:
        self._database = SqliteDatabase(getenv("DATABASE_PATH", "cibo_database.db"))

        self._telnet = server_config.telnet
        self._world = server_config.world
        self._output = server_config.output

        self._event_processor = EventProcessor(server_config)

        self._tick = TickEvent(server_config)
        self._tick_thread = Thread(target=self._start_tick_timers)

        self._spawn = SpawnEvent(server_config)

        self._thread = Thread(target=self._start_server)
        self._status = self.Status.STOPPED

    @property
    def is_running(self) -> bool:
        """Check if the server is active and listening.

        Returns:
            bool: Is the server is running or not.
        """

        return self._status is self.Status.RUNNING

    def _start_tick_timers(self) -> None:
        """Start the tick timers, that carry out scheduled actions."""

        while self.is_running:
            self._tick.process()

            sleep(1)

    def _start_server(self) -> None:
        """Start the telnet server and begin listening for events. Process any new
        events received using the event processor.
        """

        self._status = self.Status.STARTING_UP
        self._telnet.listen()
        self._status = self.Status.RUNNING

        self._tick_thread.start()

        self._spawn.process()

        while self.is_running:
            self._telnet.update()
            self._event_processor.process()

            sleep(0.05)

    def create_db(self) -> None:
        """Create the sqlite DB and necessary tables."""

        self._database.connect()
        self._database.create_tables([Player, Item, Npc])

    def start(self) -> None:
        """Create a thread and start the server."""

        if self._status is self.Status.STOPPED:
            self._thread.start()

    def stop(self) -> None:
        """Stop the currently running server and end the thread."""

        if self.is_running and self._thread:
            self._status = self.Status.SHUTTING_DOWN

            self._tick_thread.join()

            self._telnet.shutdown()
            self._thread.join()

            self._status = self.Status.STOPPED
