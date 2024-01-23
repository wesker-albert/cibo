"""Open a closed door or object."""

from typing import List, Tuple

from cibo.actions import Action
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


class Open(Action):
    """Open a closed door or object."""

    @property
    def aliases(self) -> List[str]:
        return ["open"]

    @property
    def required_args(self) -> List[str]:
        return []

    def _missing_args_message(self, user_name: str) -> Tuple[Message, Message]:
        """No arguments were provided."""

        return (
            Message(
                "You open your mouth and let out a loud belch. If anyone else is in "
                "the room, they probably heard it..."
            ),
            Message(f"[cyan]{user_name}[/] burps loudly. How disgusting..."),
        )

    @property
    def _exit_not_found_message(self) -> Message:
        """No exit in the given direction."""

        return Message("There's nothing to open.")

    def _door_is_locked_message(self, door_name: str) -> Message:
        """The door is locked."""

        return Message(f"{door_name.capitalize()} is locked.")

    def _opening_door_message(
        self, user_name: str, door_name: str
    ) -> Tuple[Message, Message, Message]:
        """Successfully opening the door."""

        return (
            Message(f"You open {door_name}."),
            Message(f"[cyan]{user_name}[/] opens {door_name}."),
            Message(f"{door_name.capitalize()} opens."),
        )

    def _door_is_open_message(self, door_name: str) -> Message:
        """The door is already open."""

        return Message(f"{door_name.capitalize()} is already open.")

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

            if not args:
                raise ActionMissingArguments

            room = self.rooms.get_by_id(client.user.current_room_id)
            exit_ = room.get_direction_exit(args[0])
            door = self.doors.get_by_room_ids(room.id_, exit_.id_)

            door.raise_status()

        except ActionMissingArguments:
            missing_args_message = self._missing_args_message(client.user.name)

            self.comms.send_to_vicinity(
                MessageRoute(missing_args_message[0], client=client),
                MessageRoute(
                    missing_args_message[1], ids=[client.user.current_room_id]
                ),
            )

        except (ClientNotLoggedIn, RoomNotFound):
            self.comms.send_prompt(client)

        except (ExitNotFound, DoorNotFound):
            self.comms.send_to_client(
                MessageRoute(self._exit_not_found_message, client=client)
            )

        except DoorIsLocked:
            self.comms.send_to_client(
                MessageRoute(self._door_is_locked_message(door.name), client=client)
            )

        except DoorIsOpen:
            self.comms.send_to_client(
                MessageRoute(self._door_is_open_message(door.name), client=client)
            )

        except DoorIsClosed:
            door.open_()

            opening_door_message = self._opening_door_message(
                client.user.name, door.name
            )

            self.comms.send_to_vicinity(
                MessageRoute(opening_door_message[0], client=client),
                MessageRoute(opening_door_message[1], ids=[room.id_]),
                MessageRoute(opening_door_message[2], ids=[exit_.id_]),
            )
