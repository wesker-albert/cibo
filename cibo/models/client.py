"""Client model"""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from _socket import socket

from cibo.models.player import Player


@dataclass
class Client:
    """Represents a client connected to the server"""

    id_: UUID
    socket: socket
    address: str
    buffer: str
    last_check: float
    player: Optional[Player]
