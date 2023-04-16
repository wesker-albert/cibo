from dataclasses import dataclass
from typing import List
from uuid import uuid4


@dataclass
class Npc:
    """Represents a non-player character"""

    uuid: uuid4
    name: str
    prefix: str
    description: str
    look: str
    allowed_rooms: List[int]
    start_room: int
    wander_freq: int
    phrases: List[str]
    speech_freq: int
