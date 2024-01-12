from tests.conftest import EntityInterfaceFactory


class TestEntityInterface(EntityInterfaceFactory):
    def test_entities_motd(self):
        assert self.entities.motd == "Welcome to the server!"
