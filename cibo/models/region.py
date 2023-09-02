"""A Region is a group of multiple Sectors."""

from dataclasses import dataclass
from typing import List

from cibo.models.flag import RoomFlag


@dataclass
class Region:
    """A group of sectors, thus a large group of rooms."""

    id_: int
    name: str
    description: str
    flags: List[RoomFlag]
