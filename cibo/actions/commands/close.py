"""Close an open door or object."""

from typing import List, Tuple

from cibo.actions._base_ import Action
from cibo.exceptions import (
    ActionMissingArguments,
    ClientNotLoggedIn,
    DoorIsClosed,
    DoorIsLocked,
    DoorIsOpen,
    DoorNotFound,
    ExitNotFound,
    RoomNotFound,
)
from cibo.models.client import Client
from cibo.models.message import Message, MessageRoute


class Close(Action):
    """Close an open door or object."""

    def aliases(self) -> List[str]:
        return ["close"]

    def required_args(self) -> List[str]:
        return []

    @property
    def _missing_args_message(self) -> Message:
        """No arguments were provided."""

        return Message("You close your eyes and daydream about money and success.")

    @property
    def _exit_not_found_message(self) -> Message:
        """No exit in the given direction."""

        return Message("There's nothing to close.")

    def _door_is_closed_message(self, door_name: str) -> Message:
        """The door is already closed."""

        return Message(f"{door_name.capitalize()} is already closed.")

    def _door_closes_message(
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
            self.comms.send_to_client(
                MessageRoute(self._missing_args_message, client=client)
            )

        except (ClientNotLoggedIn, RoomNotFound):
            self.comms.send_prompt(client)

        except (ExitNotFound, DoorNotFound):
            self.comms.send_to_client(
                MessageRoute(self._exit_not_found_message, client=client)
            )

        except (DoorIsClosed, DoorIsLocked):
            self.comms.send_to_client(
                MessageRoute(self._door_is_closed_message(door.name), client=client)
            )

        except DoorIsOpen:
            door.close()

            door_closes_message = self._door_closes_message(
                door.name, client.player.name
            )

            self.comms.send_to_vicinity(
                MessageRoute(door_closes_message[0], client=client),
                MessageRoute(door_closes_message[1], ids=[room.id_]),
                MessageRoute(door_closes_message[2], ids=[exit_.id_]),
            )
