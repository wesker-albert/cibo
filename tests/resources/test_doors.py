from pytest import raises

from cibo.exception import ResourceNotFound
from cibo.models.door import Door, DoorFlag
from cibo.resources.doors import Doors


def test_get_by_room_ids(doors: Doors):
    door = doors.get_by_room_ids(1, 7)

    assert door == Door(name="small trapdoor", room_ids=[1, 7], flags=[DoorFlag.CLOSED])


def test_get_by_room_ids_not_found(doors: Doors):
    with raises(ResourceNotFound):
        _door = doors.get_by_room_ids(10, 14)


def test_is_door_closed(doors: Doors):
    door = Door(name="small trapdoor", room_ids=[1, 7], flags=[DoorFlag.CLOSED])

    assert doors.is_door_closed(door)


def test_is_door_closed_no_door(doors: Doors):
    door = None

    assert not doors.is_door_closed(door)


def test_is_door_open(doors: Doors):
    door = Door(name="small trapdoor", room_ids=[1, 7], flags=[DoorFlag.CLOSED])

    assert not doors.is_door_open(door)


def test_is_door_open_no_door(doors: Doors):
    door = None

    assert not doors.is_door_open(door)


def test_is_door_locked(doors: Doors):
    door = Door(
        name="small trapdoor", room_ids=[1, 7], flags=[DoorFlag.CLOSED, DoorFlag.LOCKED]
    )

    assert doors.is_door_locked(door)


def test_is_door_locked_no_door(doors: Doors):
    door = None

    assert not doors.is_door_locked(door)


def test_close_door(doors: Doors):
    door = Door(name="small trapdoor", room_ids=[1, 7], flags=[DoorFlag.OPEN])

    doors.close_door(door)

    assert door.flags == [DoorFlag.CLOSED]


def test_open_door(doors: Doors):
    door = Door(name="small trapdoor", room_ids=[1, 7], flags=[DoorFlag.CLOSED])

    doors.open_door(door)

    assert door.flags == [DoorFlag.OPEN]
