"""The Output class provides message formatting and isolation logic, ensuring
that messages have a uniform style and reach only the clients they are intended to.
"""


from cibo.messages.private import Private
from cibo.messages.room import Room
from cibo.messages.vicinity import Vicinity
from cibo.telnet import TelnetServer


class Output:
    """Responsible for constructing messages that are sent to clients.

    Args:
        telnet (TelnetServer): The telnet server to use when outputting messages.
    """

    def __init__(self, telnet: TelnetServer) -> None:
        self._telnet = telnet

        self.send_private_message = Private(self._telnet).send
        self.send_room_message = Room(self._telnet).send
        self.send_vicinity_message = Vicinity(self._telnet).send
