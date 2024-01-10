from tests.conftest import SpawnFactory


class TestSpawns(SpawnFactory):
    def test_spawns_get_all(self):
        fetched_spawn = self.world.spawns.get_all()

        assert fetched_spawn == self.spawns
