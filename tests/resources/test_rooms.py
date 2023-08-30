from pytest import raises

from cibo.exception import RoomNotFound
from tests.conftest import RoomFactory, WorldFactory


class TestRooms(WorldFactory, RoomFactory):
    def test_rooms_get_by_id(self):
        fetched_room = self.world.rooms.get_by_id(1)

        assert fetched_room == self.room

    def test_rooms_get_by_id_not_found(self):
        with raises(RoomNotFound):
            _room = self.world.rooms.get_by_id(7373547567)
