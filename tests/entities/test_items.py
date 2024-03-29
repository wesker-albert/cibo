from pytest import raises

from cibo.exceptions import ItemNotFound
from tests.conftest import ItemFactory


class TestItems(ItemFactory):
    def test_items_get_by_id(self):
        item = self.entities.items.get_by_id(1)

        assert item == self.item

    def test_items_get_by_id_not_found(self):
        with raises(ItemNotFound):
            _item = self.entities.items.get_by_id(939883539365)
