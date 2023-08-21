from cibo.models.data.item import Item


class TestDataItem:
    def test_data_item_get_by_room_id(self):
        items = Item.get_by_room_id(1)

        assert len(items) == 1
        assert items[0].item_id == 1
