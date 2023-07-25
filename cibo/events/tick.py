"""Tick timers, that execute recurring Actions with varying frequency."""


from threading import Thread

from schedule import every, run_pending

from cibo.actions.__action__ import Action
from cibo.actions.scheduled.every_minute import EveryMinute
from cibo.actions.scheduled.every_second import EverySecond
from cibo.events.__event__ import Event
from cibo.resources.world import World
from cibo.telnet import TelnetServer


class TickEvent(Event):
    """Tick timers, that execute recurring Actions with varying frequency."""

    def __init__(self, telnet: TelnetServer, world: World):
        super().__init__(telnet, world)

        # schedule each of our tick Actions for processing
        every().second.do(
            self._process_tick, self._every_second, self._telnet, self._world
        )
        every().minute.do(
            self._process_tick, self._every_minute, self._telnet, self._world
        )

    @staticmethod
    def _process_tick(action: type[Action], telnet: TelnetServer, world: World):
        """This processes our tick schedules in parallel, rather than serially.
        That way our intervals are as accurate as possible.

        Args:
            action (type[Action]): The tick Action to process.
            telnet (TelnetServer): The Telnet server to use when executing the Action.
            world (World): The World as we know it.
        """

        thread = Thread(target=action, args=[telnet, world])
        thread.start()

    @staticmethod
    def _every_second(telnet: TelnetServer, world: World):
        """A tick scheduled for every second."""

        for client in telnet.get_connected_clients():
            EverySecond(telnet, world).process(client, None, [])

    @staticmethod
    def _every_minute(telnet: TelnetServer, world: World):
        """A tick scheduled for every minute."""

        for client in telnet.get_connected_clients():
            EveryMinute(telnet, world).process(client, None, [])

    def process(
        self,
    ) -> None:
        # don't tick if no clients are connected, to conserve system resources
        if len(self._telnet.get_connected_clients()) > 0:
            run_pending()
