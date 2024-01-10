from pytest import raises

from cibo.exceptions import SectorNotFound
from tests.conftest import SectorFactory


class TestSectors(SectorFactory):
    def test_sectors_get_by_id(self):
        fetched_sector = self.world.sectors.get_by_id(1)

        assert fetched_sector == self.sector

    def test_sectors_get_by_id_not_found(self):
        with raises(SectorNotFound):
            _sector = self.world.sectors.get_by_id(98736)
