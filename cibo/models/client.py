"""Client models"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import UUID

from _socket import socket

from cibo.models.player import Player


class ClientLoginState(int, Enum):
    """The different login states a client can be in."""

    PRE_LOGIN = 1
    ACCOUNT_CREATION = 2
    LOGGED_IN = 3


@dataclass
class Client:
    """Represents a client connected to the server."""

    id_: UUID
    socket: socket
    address: str
    buffer: str
    last_check: float
    login_state: ClientLoginState
    player: Optional[Player]
