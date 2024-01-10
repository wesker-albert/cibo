from pytest import raises

from cibo.exceptions import RegionNotFound
from tests.conftest import RegionFactory


class TestRegions(RegionFactory):
    def test_regions_get_by_id(self):
        fetched_region = self.world.regions.get_by_id(1)

        assert fetched_region == self.region

    def test_regions_get_by_id_not_found(self):
        with raises(RegionNotFound):
            _region = self.world.regions.get_by_id(4721)
