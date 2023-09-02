"""A Sector is a subset of rooms with, certain shared behaviors."""

from dataclasses import dataclass
from typing import List

from cibo.models.flag import RoomFlag


@dataclass
class Sector:
    """A subset of rooms with certain shared behaviors."""

    id_: int
    name: str
    description: str
    room_ids: List[int]
    flags: List[RoomFlag]
