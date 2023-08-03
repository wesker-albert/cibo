"""Close an open door or object."""

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


class Close(Action):
    """Close an open door or object."""

    def aliases(self) -> List[str]:
        return ["close"]

    def required_args(self) -> List[str]:
        return []

    @property
    def no_args_msg(self) -> str:
        """No arguments were provided."""

        return "You close your eyes and daydream about money and success."

    @property
    def not_exit_msg(self) -> str:
        """No exit in the given direction."""

        return "There's nothing to close."

    def door_is_closed_msg(self, door_name: str) -> str:
        """The door is already closed."""

        return f"The [magenta]{door_name}[/] is already closed."

    def door_closes_msg(self, door_name: str, player_name: str) -> Announcement:
        """The door is closed by the Player."""

        return Announcement(
            f"You close the [magenta]{door_name}[/].",
            f"[cyan]{player_name}[/] closes a [magenta]{door_name}[/].",
            f"A [magenta]{door_name}[/] closes.",
        )

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
            self.send.private(client, self.no_args_msg)

        except (NotLoggedIn, RoomNotFound):
            self.send.prompt(client)

        except (ExitNotFound, DoorNotFound):
            self.send.private(client, self.not_exit_msg)

        else:
            if self.doors.is_door_closed(door):
                self.send.private(client, self.door_is_closed_msg(door.name))
                return

            if self.doors.is_door_open(door):
                self.doors.close_door(door)

                door_closes_msg = self.door_closes_msg(door.name, client.player.name)

                self.send.private(client, door_closes_msg.to_self)
                self.send.local(room.id_, door_closes_msg.to_room, [client])
                self.send.local(exit_.id_, door_closes_msg.to_adjoining_room, [client])
