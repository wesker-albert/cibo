"""Open a closed door or object."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import (
    ActionMissingArguments,
    ClientNotLoggedIn,
    DoorIsClosed,
    DoorIsLocked,
    DoorIsOpen,
    DoorNotFound,
    ExitNotFound,
    RoomNotFound,
)
from cibo.output import Announcement, Message


class Open(Action):
    """Open a closed door or object."""

    def aliases(self) -> List[str]:
        return ["open"]

    def required_args(self) -> List[str]:
        return []

    def missing_args_message(self, player_name: str) -> Announcement:
        """No arguments were provided."""

        return Announcement(
            "You open your mouth and let out a loud belch. If anyone else is in the "
            "room, they probably heard it...",
            f"[cyan]{player_name}[/] burps loudly. How disgusting...",
        )

    @property
    def exit_not_found_message(self) -> Message:
        """No exit in the given direction."""

        return Message("There's nothing to open.")

    def door_is_locked_message(self, door_name: str) -> Message:
        """The door is locked."""

        return Message(f"{door_name.capitalize()} is locked.")

    def opening_door_message(self, player_name: str, door_name: str) -> Announcement:
        """Successfully opening the door."""

        return Announcement(
            f"You open {door_name}.",
            f"[cyan]{player_name}[/] opens {door_name}.",
            f"{door_name.capitalize()} opens.",
        )

    def door_is_open_message(self, door_name: str) -> Message:
        """The door is already open."""

        return Message(f"{door_name.capitalize()} is already open.")

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

            if not args:
                raise ActionMissingArguments

            room = self.rooms.get_by_id(client.player.current_room_id)
            exit_ = room.get_direction_exit(args[0])
            door = self.doors.get_by_room_ids(room.id_, exit_.id_)

            door.raise_status()

        except ActionMissingArguments:
            self.output.send_local_announcement(
                self.missing_args_message(client.player.name),
                client,
                client.player.current_room_id,
            )

        except (ClientNotLoggedIn, RoomNotFound):
            self.output.send_prompt(client)

        except (ExitNotFound, DoorNotFound):
            self.output.send_private_message(client, self.exit_not_found_message)

        except DoorIsLocked:
            self.output.send_private_message(
                client, self.door_is_locked_message(door.name)
            )

        except DoorIsOpen:
            self.output.send_private_message(
                client, self.door_is_open_message(door.name)
            )

        except DoorIsClosed:
            door.open_()

            self.output.send_local_announcement(
                self.opening_door_message(client.player.name, door.name),
                client,
                room.id_,
                exit_.id_,
            )
