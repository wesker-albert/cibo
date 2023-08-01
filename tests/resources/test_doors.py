from pytest import raises

from cibo.exception import ResourceNotFound
from cibo.models.door import Door, DoorFlag
from tests.conftest import WorldFactory


class TestDoors(WorldFactory):
    def test_get_by_room_ids(self):
        door = self.doors.get_by_room_ids(1, 7)

        assert door == Door(
            name="small trapdoor", room_ids=[1, 7], flags=[DoorFlag.CLOSED]
        )

    def test_get_by_room_ids_not_found(self):
        with raises(ResourceNotFound):
            _door = self.doors.get_by_room_ids(10, 14)

    def test_is_door_closed(self):
        door = Door(name="small trapdoor", room_ids=[1, 7], flags=[DoorFlag.CLOSED])

        assert self.doors.is_door_closed(door)

    def test_is_door_closed_no_door(self):
        door = None

        assert not self.doors.is_door_closed(door)

    def test_is_door_open(self):
        door = Door(name="small trapdoor", room_ids=[1, 7], flags=[DoorFlag.CLOSED])

        assert not self.doors.is_door_open(door)

    def test_is_door_open_no_door(self):
        door = None

        assert not self.doors.is_door_open(door)

    def test_is_door_locked(self):
        door = Door(
            name="small trapdoor",
            room_ids=[1, 7],
            flags=[DoorFlag.CLOSED, DoorFlag.LOCKED],
        )

        assert self.doors.is_door_locked(door)

    def test_is_door_locked_no_door(self):
        door = None

        assert not self.doors.is_door_locked(door)

    def test_close_door(self):
        door = Door(name="small trapdoor", room_ids=[1, 7], flags=[DoorFlag.OPEN])

        self.doors.close_door(door)

        assert door.flags == [DoorFlag.CLOSED]

    def test_open_door(self):
        door = Door(name="small trapdoor", room_ids=[1, 7], flags=[DoorFlag.CLOSED])

        self.doors.open_door(door)

        assert door.flags == [DoorFlag.OPEN]
