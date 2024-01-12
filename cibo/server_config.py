"""The configuration object which supplies all the necessary objects that the
server needs to function, and to process actions and events.
"""

from dataclasses import dataclass

from cibo.comms._interface_ import CommsInterface
from cibo.entities.world import World
from cibo.telnet import TelnetServer


@dataclass
class ServerConfig:
    """The configuration object which supplies all the necessary objects that the
    server needs to function, and to process actions and events.
    """

    telnet: TelnetServer
    world: World
    comms_interface: CommsInterface