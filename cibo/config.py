""" Used to consolodate the various objects necessary, to launch and orchestrate
the server, it's events, etc.
"""

from dataclasses import dataclass

from cibo.output import Output
from cibo.resources.world import World
from cibo.telnet import TelnetServer


@dataclass
class ServerConfig:
    """The configuration object for our server."""

    telnet: TelnetServer
    world: World
    output: Output
