"""A Region is a group of multiple Sectors.

This is a collection of all the Regions that exist in the World.
"""

from typing import List

from cibo.exception import RegionNotFound
from cibo.models.flag import RoomFlag
from cibo.models.region import Region
from cibo.resources.__resource__ import Resource


class Regions(Resource):
    """All the Regions that exist in the World."""

    def __init__(self, regions_file: str):
        self._regions: List[Region] = self._generate_resources(regions_file)

    def _create_resource_from_dict(self, resource: dict) -> Region:
        region = resource

        return Region(
            id_=region["id"],
            name=region["name"],
            description=region["description"],
            flags=[RoomFlag(flag) for flag in region["flags"]],
        )

    def get_by_id(self, id_: int) -> Region:
        """Get a Region by its ID.

        Args:
            id_ (int): The ID of the Region you're looking for.

        Raises:
            RegionNotFound: No Region found for the given ID.

        Returns:
            Region: The matching Region.
        """

        for region in self._regions:
            if region.id_ == id_:
                return region

        raise RegionNotFound
