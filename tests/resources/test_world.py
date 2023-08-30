from tests.conftest import WorldFactory


class TestWorld(WorldFactory):
    def test_world_motd(self):
        assert self.world.motd == "Welcome to the server!"
