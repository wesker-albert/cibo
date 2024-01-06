"""Close an open door or object."""

from typing import List, Tuple

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
from cibo.models.message import Message, MessageRoute


class Close(Action):
    """Close an open door or object."""

    def aliases(self) -> List[str]:
        return ["close"]

    def required_args(self) -> List[str]:
        return []

    @property
    def missing_args_message(self) -> Message:
        """No arguments were provided."""

        return Message("You close your eyes and daydream about money and success.")

    @property
    def exit_not_found_message(self) -> Message:
        """No exit in the given direction."""

        return Message("There's nothing to close.")

    def door_is_closed_message(self, door_name: str) -> Message:
        """The door is already closed."""

        return Message(f"{door_name.capitalize()} is already closed.")

    def door_closes_message(
        self, door_name: str, player_name: str
    ) -> Tuple[Message, Message, Message]:
        """The door is closed by the player."""

        return (
            Message(f"You close {door_name}."),
            Message(f"[cyan]{player_name}[/] closes {door_name}."),
            Message(f"{door_name.capitalize()} closes."),
        )

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
            self.output.send_private_message(client, self.missing_args_message)

        except (ClientNotLoggedIn, RoomNotFound):
            self.output.send_prompt(client)

        except (ExitNotFound, DoorNotFound):
            self.output.send_private_message(client, self.exit_not_found_message)

        except (DoorIsClosed, DoorIsLocked):
            self.output.send_private_message(
                client, self.door_is_closed_message(door.name)
            )

        except DoorIsOpen:
            door.close()

            door_closes_message = self.door_closes_message(
                door.name, client.player.name
            )

            self.output.send_vicinity_message(
                client,
                door_closes_message[0],
                MessageRoute(room.id_, door_closes_message[1]),
                MessageRoute(exit_.id_, door_closes_message[2]),
            )
