"""Player model"""

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4


@dataclass
class Player:
    """Represents a human-controlled player character"""

    uuid: uuid4
    name: str
    created_at: datetime
