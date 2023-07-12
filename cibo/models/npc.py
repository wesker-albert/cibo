"""An Npc is a non-player character, that a player might encounter while exploring
the world. Some Npcs can be interacted with, in varying ways.
"""

from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class Npc:
    """Represents a non-player character."""

    uuid: UUID
    name: str
    prefix: str
    description: str
    look: str
    allowed_rooms: List[int]
    start_room: int
    wander_freq: int
    phrases: List[str]
    speech_freq: int
