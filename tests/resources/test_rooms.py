from pytest import raises

from cibo.exception import ResourceNotFound
from cibo.models.room import Direction, Room, RoomDescription, RoomExit
from tests.conftest import WorldFactory


class TestRooms(WorldFactory):
    def test_get_by_id(self):
        room = self.rooms.get_by_id(1)

        assert room == Room(
            id_=1,
            name="A Room Marked #1",
            description=RoomDescription(
                normal="The walls and floor of this room are a bright, sterile white. You feel as if you are inside a simulation.",
                extra=None,
                night=None,
                under=None,
                behind=None,
                above=None,
                smell=None,
                listen=None,
            ),
            exits=[
                RoomExit(direction=Direction.NORTH, id_=2, description=None),
                RoomExit(direction=Direction.EAST, id_=3, description=None),
                RoomExit(direction=Direction.SOUTH, id_=4, description=None),
                RoomExit(direction=Direction.WEST, id_=5, description=None),
                RoomExit(direction=Direction.UP, id_=6, description=None),
                RoomExit(direction=Direction.DOWN, id_=7, description=None),
            ],
        )

    def test_get_by_id_not_found(self):
        with raises(ResourceNotFound):
            _room = self.rooms.get_by_id(7373547567)

    def test_get_exits(self, room: Room):
        room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
            RoomExit(direction=Direction.EAST, id_=3, description=None),
        ]

        assert self.rooms.get_exits(room) == ["east", "north"]

    def test_get_formatted_exits(self, room: Room):
        room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
            RoomExit(direction=Direction.EAST, id_=3, description=None),
        ]

        assert self.rooms.get_formatted_exits(room) == "[green]Exits:[/] east, north"

    def test_get_formatted_exits_single_exit(self, room: Room):
        room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
        ]

        assert self.rooms.get_formatted_exits(room) == "[green]Exit:[/] north"

    def test_get_formatted_exits_none(self, room: Room):
        assert self.rooms.get_formatted_exits(room) == "[green]Exits:[/] none"

    def test_get_direction_exit(self, room: Room):
        room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
            RoomExit(direction=Direction.EAST, id_=3, description=None),
        ]

        assert self.rooms.get_direction_exit(room, "n") == RoomExit(
            direction=Direction.NORTH, id_=2, description=None
        )

    def test_get_direction_exit_not_found(self, room: Room):
        room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
            RoomExit(direction=Direction.EAST, id_=3, description=None),
        ]

        assert not self.rooms.get_direction_exit(room, "w")
