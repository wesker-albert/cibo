"""Open a closed door or object."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import (
    DoorNotFound,
    ExitNotFound,
    MissingArguments,
    NotLoggedIn,
    RoomNotFound,
)
from cibo.models.announcement import Announcement


class Open(Action):
    """Open a closed door or object."""

    def aliases(self) -> List[str]:
        return ["open"]

    def required_args(self) -> List[str]:
        return []

    def no_args_msg(self, player_name: str) -> Announcement:
        """No arguments were provided."""

        return Announcement(
            "You open your mouth and let out a loud belch. If anyone else is in the "
            "room, they probably heard it...",
            f"[cyan]{player_name}[/] burps loudly. How disgusting...",
        )

    @property
    def not_exit_msg(self) -> str:
        """No exit in the given direction."""

        return "There's nothing to open."

    def door_is_locked_msg(self, door_name: str) -> str:
        """The door is locked."""

        return f"The [magenta]{door_name}[/] is locked."

    def opening_door_msg(self, player_name: str, door_name: str) -> Announcement:
        """Successfully opening the door."""

        return Announcement(
            f"You open the [magenta]{door_name}[/].",
            f"[cyan]{player_name}[/] opens a [magenta]{door_name}[/].",
            f"A [magenta]{door_name}[/] opens.",
        )

    def door_is_open(self, door_name: str) -> str:
        """The door is already open."""

        return f"The [magenta]{door_name}[/] is already open."

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise NotLoggedIn

            if not args:
                raise MissingArguments

            room = self.rooms.get_by_id(client.player.current_room_id)
            exit_ = self.rooms.get_direction_exit(room, args[0])
            door = self.doors.get_by_room_ids(room.id_, exit_.id_)

        except MissingArguments:
            no_args_msg = self.no_args_msg(client.player.name)

            self.send.private(client, no_args_msg.to_self)
            self.send.local(
                client.player.current_room_id, no_args_msg.to_room, [client]
            )

        except (NotLoggedIn, RoomNotFound):
            self.send.prompt(client)

        except (ExitNotFound, DoorNotFound):
            self.send.private(client, self.not_exit_msg)

        else:
            if self.doors.is_door_locked(door):
                self.send.private(client, self.door_is_locked_msg(door.name))
                return

            if self.doors.is_door_closed(door):
                self.doors.open_door(door)

                opening_door_msg = self.opening_door_msg(client.player.name, door.name)

                self.send.private(client, opening_door_msg.to_self)
                self.send.local(room.id_, opening_door_msg.to_room, [client])
                self.send.local(exit_.id_, opening_door_msg.to_adjoining_room, [client])
                return

            if self.doors.is_door_open(door):
                self.send.private(client, self.door_is_open(door.name))
