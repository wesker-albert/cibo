from cibo.models.data import Item
from tests.conftest import DatabaseFactory


class TestDataItem(DatabaseFactory):
    def test_data_item_get_by_current_room_id(self, _fixture_database):
        items = Item.get_by_current_room_id(1)

        assert len(items) == 2
        assert items[0].item_id == 1
        assert items[1].item_id == 2
