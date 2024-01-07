"""The configuration object which supplies all the necessary objects that the
server needs to function, and to process actions and events.
"""

from dataclasses import dataclass

from cibo.output import OutputProcessor
from cibo.resources.world import World
from cibo.telnet import TelnetServer


@dataclass
class ServerConfig:
    """The configuration object which supplies all the necessary objects that the
    server needs to function, and to process actions and events.
    """

    telnet: TelnetServer
    world: World
    output_processor: OutputProcessor
