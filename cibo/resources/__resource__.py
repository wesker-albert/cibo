"""A Resource is some kind of tangible object that exists in the World, often
interactable.

Some examples of a Resource would be: a Room, Door, Item, or Npc.
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union

from cibo.models.object.door import Door
from cibo.models.object.item import Item
from cibo.models.object.room import Room


class Resource(ABC):
    """An object that exists in the World."""

    def _generate_resources(self, filename: str) -> list:
        """Generate all the resources, from the local JSON file that houses them,

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
    ) -> Union[Item, Room, Door]:  # pytest: no cover
        pass
