"""Instantiates a telnet server. Provides event processing for the telnet server, as
well as methods to control the server state.
"""

import os
from enum import Enum
from threading import Thread
from time import sleep

from peewee import SqliteDatabase

from cibo.decorator import load_environment_variables
from cibo.event import EventProcessor
from cibo.events.tick import TickEvent
from cibo.models.player import Player
from cibo.output import Output
from cibo.resources.world import World
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
    def __init__(self, telnet: TelnetServer, world: World, output: Output) -> None:
        """Creates a dormant telnet server. Once instantiated, it can be started and
        stopped.

        Args:
            telnet (TelnetServer): The TelnetServer instance to use.
            world (World): The world, and all its resources.
        """

        self._database = SqliteDatabase(os.getenv("DATABASE_PATH", "cibo_database.db"))

        self._telnet = telnet
        self._world = world
        self._output = output

        self._event_processor = EventProcessor(self._telnet, self._world, self._output)

        self._tick = TickEvent(self._telnet, self._world, self._output)
        self._tick_thread = Thread(target=self._start_tick_timers)

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
        """Start the tick timers, that carry out schedules Actions."""

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

        while self.is_running:
            self._telnet.update()
            self._event_processor.process()

            sleep(0.05)

    def create_db(self) -> None:
        """Create the sqlite DB and necessary tables."""

        self._database.connect()
        self._database.create_tables([Player])

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
