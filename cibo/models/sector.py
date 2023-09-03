"""A Sector is a subset of rooms with, certain shared behaviors."""

from dataclasses import dataclass
from typing import List

from cibo.models.flag import RoomFlag
from cibo.models.region import Region


@dataclass
class Sector:
    """A subset of rooms with certain shared behaviors."""

    id_: int
    name: str
    description: str
    region: Region
    flags: List[RoomFlag]
