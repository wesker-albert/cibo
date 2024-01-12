from pytest import raises

from cibo.exceptions import RoomNotFound
from tests.conftest import RoomFactory


class TestRooms(RoomFactory):
    def test_rooms_get_by_id(self):
        fetched_room = self.entities.rooms.get_by_id(1)

        assert fetched_room == self.room

    def test_rooms_get_by_id_not_found(self):
        with raises(RoomNotFound):
            _room = self.entities.rooms.get_by_id(7373547567)
