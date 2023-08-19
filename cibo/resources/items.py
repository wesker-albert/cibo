from typing import List

from cibo.exception import ItemNotFound
from cibo.models.object.item import Item
from cibo.resources.__resource__ import Resource


class Items(Resource):
    """All the Items that exist in the world."""

    def __init__(self, items_file: str):
        self._items: List[Item] = self._generate_resources(items_file)

    def _create_resource_from_dict(self, resource: dict) -> Item:
        item = resource

        return Item(
            id_=item["id"],
            name=item["name"],
            description=item["description"],
            is_stationary=item["is_stationary"],
            carry_limit=item.get("carry_limit", 0),
            weight=item.get("weight", 0),
        )

    def get_by_id(self, id_: int) -> Item:
        for item in self._items:
            if item.id_ == id_:
                return item

        raise ItemNotFound
