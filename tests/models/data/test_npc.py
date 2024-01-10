from cibo.models.data import Npc
from tests.conftest import DatabaseFactory


class TestDataNpc(DatabaseFactory):
    def test_data_npc_get_by_current_room_id(self, _fixture_database):
        npcs = Npc.get_by_current_room_id(1)

        assert len(npcs) == 1
        assert npcs[0].npc_id == 1

    def test_data_npc_get_by_spawn_room_id(self, _fixture_database):
        npcs = Npc.get_by_spawn_room_id(1)

        assert len(npcs) == 1
        assert npcs[0].npc_id == 1
