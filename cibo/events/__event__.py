"""Abstraction to be used as a base class for every Event."""

from abc import ABC, abstractmethod

from cibo.resources.world import World
from cibo.telnet import TelnetServer


class Event(ABC):
    """The base interface used by other Event classes."""

    def __init__(self, telnet: TelnetServer, world: World) -> None:
        self._telnet = telnet
        self._world = world

    @abstractmethod
    def process(self) -> None:
        """Processes the logic for the specific Event type."""

        pass
