from cibo.models.data.item import Item
from tests.conftest import SpawnEventFactory


class TestSpawnEvent(SpawnEventFactory):
    def test_event_spawn_process(self, _fixture_database):
        self.spawn.process()

        item = Item.get_by_id(4)
        assert item.spawn_room_id == 2