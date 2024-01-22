"""A Entity is some kind of tangible object that exists in the world, often
interactable.

Some examples of a entity would be: a room, door, item, or NPC.
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union

from cibo.models.door import Door
from cibo.models.item import Item
from cibo.models.npc import Npc
from cibo.models.region import Region
from cibo.models.room import Room
from cibo.models.sector import Sector
from cibo.models.spawn import Spawn


class Entity(ABC):
    """An object that exists in the world."""

    def _generate_entities(self, filename: str) -> list:
        """Generate all the entities, from the local JSON file that houses them.

        Returns:
            List[Room]: All the entities.
        """

        return [
            self._create_entity_from_dict(entity)
            for entity in self._get_entities_from_file(filename)
        ]

    def _get_entities_from_file(self, filename: str) -> List[dict]:
        """Loads the JSON file into a dict, then compiles each entity object into
        a list.

        Returns:
            List[dict]: The entities in raw dict format.
        """

        with open(f"{Path.cwd()}/{filename}", encoding="utf-8") as file:
            data = json.load(file)

        return next(iter(data.values()))

    @abstractmethod
    def _create_entity_from_dict(
        self, entity: dict
    ) -> Union[Item, Room, Door, Sector, Region, Npc, Spawn]:  # pytest: no cover
        pass
