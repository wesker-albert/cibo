from pytest import raises

from cibo.exception import ItemNotFound
from cibo.models.item import Item
from tests.conftest import WorldFactory


class TestItems(WorldFactory):
    def test_items_get_by_id(self):
        item = self.items.get_by_id(1)

        assert item == Item(
            id_=1,
            name="a metal fork",
            description="A pronged, metal eating utensil.",
            is_stationary=False,
            carry_limit=0,
            weight=0,
        )

    def test_items_get_by_id_not_found(self):
        with raises(ItemNotFound):
            _item = self.items.get_by_id(939883539365)
