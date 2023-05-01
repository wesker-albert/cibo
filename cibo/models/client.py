"""Client model"""

from dataclasses import dataclass
from uuid import uuid4

from cibo.models.player import Player


@dataclass
class Client:
    """Represents a client connected to the server"""

    uuid: uuid4
    host_address: str
    port: int
    player: Player
