"""Tick timers, that execute recurring Actions with varying frequency."""


from threading import Thread

from schedule import every, run_pending

from cibo.actions.__action__ import Action
from cibo.actions.scheduled.every_minute import EveryMinute
from cibo.actions.scheduled.every_second import EverySecond
from cibo.config import ServerConfig
from cibo.events.__event__ import Event


class TickEvent(Event):
    """Tick timers, that execute recurring Actions with varying frequency.

    Args:
        server_config (ServerConfig): The server configuration object.
    """

    def __init__(self, server_config: ServerConfig):
        super().__init__(server_config)

        # schedule each of our tick Actions for processing
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
            action (type[Action]): The tick Action to process.
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
        self,
    ) -> None:
        # don't tick if no clients are connected, to conserve system resources
        if len(self._telnet.get_connected_clients()) > 0:
            run_pending()
