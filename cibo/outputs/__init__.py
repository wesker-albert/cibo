"""Outputs are types of messages that can be send to clients, connected to the server.
Different output types will target different clients, depending on the routing
supplied.
"""

from cibo.outputs.private import Private
from cibo.outputs.region import Region
from cibo.outputs.room import Room
from cibo.outputs.sector import Sector
from cibo.outputs.server import Server
