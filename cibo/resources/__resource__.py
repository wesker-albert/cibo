"""A Resource is some kind of tangible object that exists in the world, often
interactable.

Some examples of a resource would be: a room, door, item, or NPC.
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Union

from cibo.models.door import Door
from cibo.models.item import Item
from cibo.models.npc import Npc
from cibo.models.region import Region
from cibo.models.room import Room
from cibo.models.sector import Sector
from cibo.models.spawn import Spawn


class Resource(ABC):
    """An object that exists in the world."""

    def _generate_resources(self, filename: str) -> list:
        """Generate all the resources, from the local JSON file that houses them.

        Returns:
            List[Room]: All the resources.
        """

        return [
            self._create_resource_from_dict(resource)
            for resource in self._get_resources_from_file(filename)
        ]

    def _get_resources_from_file(self, filename: str) -> List[dict]:
        """Loads the JSON file into a dict, then compiles each resource object into
        a list.

        Returns:
            List[dict]: The resources in raw dict format.
        """

        with open(f"{Path.cwd()}/{filename}", encoding="utf-8") as file:
            data = json.load(file)

        return next(iter(data.values()))

    @abstractmethod
    def _create_resource_from_dict(
        self, resource: dict
    ) -> Union[Item, Room, Door, Sector, Region, Npc, Spawn]:  # pytest: no cover
        pass


class Composite:
    """Resource composite methods, that we don't necessarily want inherited by all
    resource types.
    """

    def get_by_name(
        self, resources: List[Union[Item, Npc]], name: str
    ) -> Optional[Union[Item, Npc]]:
        """Finds a resource in a list of resources, with a name that matches or
        contains the provided string. If the string starts with a number followed
        by a period, that number is used as an index assuming there are multiple
        matches.


        Args:
            resources (List[Union[Item, Npc]]): The resources to search against.
            name (str): What to search for in the resource name.

        Returns:
            Optional[Union[Item, Npc]]: The matching resource, if one is found.
        """

        search_name = name
        name_segments = name.split(".")

        # after splitting on periods in the name, if the first character is a number,
        # we want to be able to target that specific index in the resources list
        if name_segments[0].isdigit():
            # a specified index of 0 (zero) returns none -- see the next comment below
            if len(name_segments) > 1 and int(name_segments[0]) > 0:
                search_name = name_segments[1]
            else:
                return None

        results = [resource for resource in resources if search_name in resource.name]

        if not results:
            return None

        if name_segments[0].isdigit():
            try:
                # we expect the initial index to be 1 (not zero) because it's
                # more intuitive from a user perspective, so we have to decrease it
                # here by 1 to be accurate against our list
                return results[(int(name_segments[0]) - 1)]

            except IndexError:
                return None

        return results[0]
