"""A Sector is a subset of rooms with, certain shared behaviors.

This is a collection of all the sectors that exist in the world.
"""

from typing import List

from cibo.entities import Entity
from cibo.entities.regions import Regions
from cibo.exceptions import SectorNotFound
from cibo.models.flag import RoomFlag
from cibo.models.sector import Sector


class Sectors(Entity):
    """All the sectors that exist in the world."""

    def __init__(self, sectors_file: str, regions: Regions):
        self._regions = regions
        self._sectors: List[Sector] = self._generate_entities(sectors_file)

    def _create_entity_from_dict(self, entity: dict) -> Sector:
        sector = entity

        return Sector(
            id_=sector["id"],
            name=sector["name"],
            description=sector["description"],
            region=self._regions.get_by_id(sector["region_id"]),
            flags=[RoomFlag(flag) for flag in sector["flags"]],
        )

    def get_by_id(self, id_: int) -> Sector:
        """Get a sector by its ID.

        Args:
            id_ (int): The sector ID you're looking for.

        Raises:
            SectorNotFound: No sector found for the given ID.

        Returns:
            Sector: The matching sector.
        """

        for sector in self._sectors:
            if sector.id_ == id_:
                return sector

        raise SectorNotFound
