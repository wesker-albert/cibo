from pytest import raises

from cibo.exception import DoorNotFound
from cibo.models.door import Door, DoorFlag
from tests.conftest import WorldFactory


class TestDoors(WorldFactory):
    def test_doors_get_by_room_ids(self):
        door = self.doors.get_by_room_ids(1, 7)

        assert door == Door(
            name="a small trapdoor", room_ids=[1, 7], flags=[DoorFlag.CLOSED]
        )

    def test_doors_get_by_room_ids_not_found(self):
        with raises(DoorNotFound):
            _door = self.doors.get_by_room_ids(10, 14)
