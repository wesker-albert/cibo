from pytest import raises

from cibo.exceptions import DoorNotFound
from tests.conftest import DoorFactory


class TestDoors(DoorFactory):
    def test_doors_get_by_room_ids(self):
        door = self.entities.doors.get_by_room_ids(1, 2)

        assert door == self.door_closed

    def test_doors_get_by_room_ids_not_found(self):
        with raises(DoorNotFound):
            _door = self.entities.doors.get_by_room_ids(10, 14)
