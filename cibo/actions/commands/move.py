"""Navigates a player between available rooms."""

from typing import List, Tuple

from cibo.actions.__action__ import Action
from cibo.actions.commands.look import Look
from cibo.exception import (
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


class Move(Action):
    """Navigates a player between available rooms."""

    def aliases(self) -> List[str]:
        return [
            "d",
            "down",
            "e",
            "east",
            "n",
            "north",
            "s",
            "south",
            "u",
            "up",
            "w",
            "west",
        ]

    def required_args(self) -> List[str]:
        return []

    @property
    def exit_not_found_message(self) -> Message:
        """No exit in the given direction."""

        return Message("You can't go that way.")

    def door_is_closed_message(self, door_name: str) -> Message:
        """There's a closed door in the way."""

        return Message(f"{door_name.capitalize()} is closed.")

    def moving_message(
        self, player_name: str, direction: str
    ) -> Tuple[Message, Message, Message]:
        """Successfully moving in the direction given."""

        return (
            Message(f"You head {direction}."),
            Message(f"[cyan]{player_name}[/] arrives."),
            Message(f"[cyan]{player_name}[/] leaves {direction}."),
        )

    def process(self, client: Client, command: str, _args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

            room = self.rooms.get_by_id(client.player.current_room_id)
            exit_ = room.get_direction_exit(command)
            door = self.doors.get_by_room_ids(room.id_, exit_.id_)

            door.raise_status()

        except (ClientNotLoggedIn, RoomNotFound):
            client.send_prompt()

        except ExitNotFound:
            self.output.private.send(
                MessageRoute(self.exit_not_found_message, client=client)
            )

        except (DoorIsClosed, DoorIsLocked):
            self.output.private.send(
                MessageRoute(self.door_is_closed_message(door.name), client=client)
            )

        except (DoorNotFound, DoorIsOpen):
            # update the player's current room to the one they're navigating to
            client.player.current_room_id = exit_.id_

            moving_message = self.moving_message(
                client.player.name, exit_.direction.name.lower()
            )

            self.output.vicinity.send(
                MessageRoute(moving_message[0], client=client),
                MessageRoute(moving_message[1], ids=[client.player.current_room_id]),
                MessageRoute(moving_message[2], ids=[room.id_]),
            )

            Look(self._server_config).process(client, None, [])
