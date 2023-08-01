from pytest import raises

from cibo.exception import ResourceNotFound
from cibo.models.room import Direction, Room, RoomDescription, RoomExit
from cibo.resources.rooms import Rooms


def test_get_by_id(rooms: Rooms):
    room = rooms.get_by_id(1)

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


def test_get_by_id_not_found(rooms: Rooms):
    with raises(ResourceNotFound):
        _room = rooms.get_by_id(7373547567)


def test_get_exits(rooms: Rooms):
    room = Room(
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
        ],
    )

    assert rooms.get_exits(room) == ["east", "north"]


def test_get_formatted_exits(rooms: Rooms):
    room = Room(
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
        ],
    )

    assert rooms.get_formatted_exits(room) == "[green]Exits:[/] east, north"


def test_get_formatted_exits_single_exit(rooms: Rooms):
    room = Room(
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
        ],
    )

    assert rooms.get_formatted_exits(room) == "[green]Exit:[/] north"


def test_get_formatted_exits_none(rooms: Rooms):
    room = Room(
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
        exits=[],
    )

    assert rooms.get_formatted_exits(room) == "[green]Exits:[/] none"


def test_get_direction_exit(rooms: Rooms):
    room = Room(
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
        ],
    )

    assert rooms.get_direction_exit(room, "n") == RoomExit(
        direction=Direction.NORTH, id_=2, description=None
    )


def test_get_direction_exit_not_found(rooms: Rooms):
    room = Room(
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
        ],
    )

    assert not rooms.get_direction_exit(room, "w")
