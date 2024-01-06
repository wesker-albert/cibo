from abc import ABC

from cibo.telnet import TelnetServer


class Message(ABC):
    def __init__(self, telnet: TelnetServer):
        self._telnet = telnet
