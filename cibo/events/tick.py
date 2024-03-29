"""Tick timers, that execute recurring actions with varying frequency."""


from threading import Thread
from typing import Any, Optional

from schedule import every, run_pending

from cibo.actions import Action
from cibo.actions.scheduled import EveryMinute, EverySecond
from cibo.events import Event, EventPayload
from cibo.server_config import ServerConfig


class TickEvent(Event):
    """Tick timers, that execute recurring actions with varying frequency.

    Args:
        server_config (ServerConfig): The server configuration object.
        signal_name (str): The event signal name to subscribe to.
    """

    def __init__(self, server_config: ServerConfig, signal_name: str):
        super().__init__(server_config, signal_name)

        # schedule each of our tick actions for processing
        every().second.do(
            self._process_tick,
            self._every_second,
            server_config,
        )
        every().minute.do(
            self._process_tick,
            self._every_minute,
            server_config,
        )

    @staticmethod
    def _process_tick(action: type[Action], server_config: ServerConfig) -> None:
        """This processes our tick schedules in parallel, rather than serially.
        That way our intervals are as accurate as possible.

        Args:
            action (type[Action]): The tick action to process.
            server_config (ServerConfig): The server configuration object.
        """

        thread = Thread(target=action, args=[server_config])
        thread.start()

    @staticmethod
    def _every_second(server_config: ServerConfig) -> None:
        """A tick scheduled for every second."""

        for client in server_config.telnet.get_connected_clients():
            EverySecond(server_config).process(client, None, [])

    @staticmethod
    def _every_minute(server_config: ServerConfig) -> None:
        """A tick scheduled for every minute."""

        for client in server_config.telnet.get_connected_clients():
            EveryMinute(server_config).process(client, None, [])

    def process(
        self, _sender: Any = None, _payload: Optional[EventPayload] = None
    ) -> None:
        # don't tick if no clients are connected, to conserve system entities
        if len(self._telnet.get_connected_clients()) > 0:
            run_pending()
