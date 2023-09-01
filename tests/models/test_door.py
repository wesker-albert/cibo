from pytest import raises

from cibo.exception import DoorIsClosed, DoorIsLocked, DoorIsOpen
from cibo.models.door import Door, DoorFlag
from tests.conftest import DoorFactory


class TestDoor(DoorFactory):
    def test_door_is_closed(self):
        assert self.door_closed.is_closed

    def test_door_is_open(self):
        assert not self.door_closed.is_open

    def test_door_is_locked(self):
        assert self.door_locked.is_locked

    def test_door_close(self):
        door = self.door_open

        door.close()

        assert door.flags == [DoorFlag.CLOSED]

    def test_door_open(self):
        door = self.door_closed

        door.open_()

        assert door.flags == [DoorFlag.OPEN]

    def test_door_raise_status(self):
        with raises(DoorIsClosed):
            self.door_closed.raise_status()

        with raises(DoorIsOpen):
            self.door_open.raise_status()

        with raises(DoorIsLocked):
            self.door_locked.raise_status()

        door = Door(name="a door missing flags", room_ids=[1, 2], flags=[])
        door.raise_status()
