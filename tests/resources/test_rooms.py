from pytest import raises

from cibo.exception import ExitNotFound, RoomNotFound
from cibo.models.room import Direction, Room, RoomExit
from tests.conftest import WorldFactory


class TestRooms(WorldFactory):
    def test_rooms_get_by_id(self, room: Room):
        fetched_room = self.rooms.get_by_id(1)

        assert fetched_room == room

    def test_rooms_get_by_id_not_found(self):
        with raises(RoomNotFound):
            _room = self.rooms.get_by_id(7373547567)

    def test_rooms_get_exits(self, room: Room):
        room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
            RoomExit(direction=Direction.EAST, id_=3, description=None),
        ]

        assert self.rooms.get_exits(room) == ["east", "north"]

    def test_rooms_get_formatted_exits(self, room: Room):
        room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
            RoomExit(direction=Direction.EAST, id_=3, description=None),
        ]

        assert self.rooms.get_formatted_exits(room) == "[green]Exits:[/] east, north"

    def test_rooms_get_formatted_exits_single_exit(self, room: Room):
        room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
        ]

        assert self.rooms.get_formatted_exits(room) == "[green]Exit:[/] north"

    def test_rooms_get_formatted_exits_none(self, room: Room):
        room.exits = []

        assert self.rooms.get_formatted_exits(room) == "[green]Exits:[/] none"

    def test_rooms_get_direction_exit(self, room: Room):
        room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
            RoomExit(direction=Direction.EAST, id_=3, description=None),
        ]

        assert self.rooms.get_direction_exit(room, "n") == RoomExit(
            direction=Direction.NORTH, id_=2, description=None
        )

    def test_rooms_get_direction_exit_not_found(self, room: Room):
        room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
            RoomExit(direction=Direction.EAST, id_=3, description=None),
        ]

        with raises(ExitNotFound):
            self.rooms.get_direction_exit(room, "w")
