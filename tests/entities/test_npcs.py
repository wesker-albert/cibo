from pytest import raises

from cibo.exceptions import NpcNotFound
from tests.conftest import NpcFactory


class TestNpcs(NpcFactory):
    def test_npcs_get_by_id(self):
        npc = self.entities.npcs.get_by_id(1)

        assert npc == self.npc

    def test_npcs_get_by_id_not_found(self):
        with raises(NpcNotFound):
            _npc = self.entities.npcs.get_by_id(75758)
