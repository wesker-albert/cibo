"""An item is an in-game piece of inventory, that can be picked up, carried, and
often used by a user.

This is a collection of all the items that exist in the world.
"""

from typing import List

from cibo.entities import Entity
from cibo.exceptions import ItemNotFound
from cibo.models.data.item import Item as ItemData
from cibo.models.item import EntityDescription, Item


class Items(Entity):
    """All the items that exist in the world."""

    def __init__(self, items_file: str):
        self._items: List[Item] = self._generate_entities(items_file)

    def _create_entity_from_dict(self, entity: dict) -> Item:
        item = entity

        return Item(
            id_=item["id"],
            name=item["name"],
            description=EntityDescription(
                room=item["description"]["room"],
                look=item["description"]["look"],
            ),
            is_stationary=item["is_stationary"],
            carry_limit=item.get("carry_limit", 0),
            weight=item.get("weight", 0),
        )

    def get_by_id(self, id_: int) -> Item:
        """Get an item by it's ID.

        Args:
            id_ (int): The item ID you're looking for.

        Raises:
            ItemNotFound: The item does not exist in the world.

        Returns:
            Item: The matched item.
        """

        for item in self._items:
            if item.id_ == id_:
                return item

        raise ItemNotFound

    def get_from_dataset(self, items_dataset: List[ItemData]) -> List[Item]:
        """Compiles a list of items, using the IDs from a set of corresponding
        item data models.

        Args:
            items_dataset (List[ItemData]): The set of item data models.

        Returns:
            List[Item]: The compiled list of items.
        """

        return [self.get_by_id(item.item_id) for item in items_dataset]
