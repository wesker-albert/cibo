from abc import ABC, abstractmethod

from cibo.telnet import TelnetServer


class Event(ABC):
    """The base interface used by other Event classes."""

    def __init__(self, telnet: TelnetServer) -> None:
        self._telnet = telnet

    @abstractmethod
    def process(self) -> None:
        """Processes the logic for the specific event type."""

        pass
