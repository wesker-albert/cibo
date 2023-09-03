from pytest import raises

from cibo.exception import ExitNotFound
from cibo.models.direction import Direction
from cibo.models.room import RoomExit
from tests.conftest import RoomFactory


class TestRoom(RoomFactory):
    def test_rooms_get_exits(self):
        self.room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
            RoomExit(direction=Direction.EAST, id_=3, description=None),
        ]

        assert self.room.get_exits() == ["east", "north"]

    def test_rooms_get_formatted_exits(self):
        self.room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
            RoomExit(direction=Direction.EAST, id_=3, description=None),
        ]

        assert self.room.get_formatted_exits() == "[green]Exits:[/] east, north"

    def test_rooms_get_formatted_exits_single_exit(self):
        self.room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
        ]

        assert self.room.get_formatted_exits() == "[green]Exit:[/] north"

    def test_rooms_get_formatted_exits_none(self):
        self.room.exits = []

        assert self.room.get_formatted_exits() == "[green]Exits:[/] none"

    def test_rooms_get_direction_exit(self):
        self.room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
            RoomExit(direction=Direction.EAST, id_=3, description=None),
        ]

        assert self.room.get_direction_exit("n") == RoomExit(
            direction=Direction.NORTH, id_=2, description=None
        )

    def test_rooms_get_direction_exit_not_found(self):
        self.room.exits = [
            RoomExit(direction=Direction.NORTH, id_=2, description=None),
            RoomExit(direction=Direction.EAST, id_=3, description=None),
        ]

        with raises(ExitNotFound):
            self.room.get_direction_exit("w")
