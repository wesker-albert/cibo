"""Events are server occurances of different types. Events can happen as a result of
client interactions with the server, or (in future) can be scheduled based upon a
tick timer or cron.

Some events call actions directly. Others, like user input, will be ran through the
CommandProcessor to determine which action should be called.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from blinker import signal

from cibo.models.event import EventPayload
from cibo.server_config import ServerConfig


class Event(ABC):
    """The base interface used by all Event classes.

    Args:
        server_config (ServerConfig): The server configuration object.
        signal_name (str): The event signal name to subscribe to.
    """

    def __init__(self, server_config: ServerConfig, signal_name: str) -> None:
        self._server_config = server_config

        self._telnet = self._server_config.telnet
        self._entities = self._server_config.entity_interface
        self._comms = self._server_config.comms_interface

        self.signal_name = signal_name
        self._signal = signal(self.signal_name)
        self._signal.connect(self.process)

    @abstractmethod
    def process(
        self, sender: Any, payload: Optional[EventPayload]
    ) -> None:  # pytest: no cover
        """Processes the logic for the specific event type."""

        pass
