"""Navigates a player between available rooms."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.actions.commands.look import Look
from cibo.client import Client
from cibo.exception import DoorNotFound, ExitNotFound, NotLoggedIn, RoomNotFound
from cibo.models.announcement import Announcement


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
    def not_exit_msg(self) -> str:
        """No exit in the given direction."""

        return "You can't go that way."

    def door_is_closed_msg(self, door_name: str) -> str:
        """There's a closed door in the way."""

        return f"The [magenta]{door_name}[/] is closed."

    def moving_msg(self, player_name: str, direction: str) -> Announcement:
        """Successfully moving in the direction given."""

        return Announcement(
            f"You head {direction}.",
            f"[cyan]{player_name}[/] leaves {direction}.",
            f"[cyan]{player_name}[/] arrives.",
        )

    def process(self, client: Client, command: str, _args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise NotLoggedIn

            current_room = self.rooms.get_by_id(client.player.current_room_id)
            exit_ = self.rooms.get_direction_exit(current_room, command)
            door = self.doors.get_by_room_ids(current_room.id_, exit_.id_)

        except (NotLoggedIn, RoomNotFound):
            self.send.prompt(client)
            return

        except ExitNotFound:
            self.send.private(client, self.not_exit_msg)
            return

        except DoorNotFound:
            door = None

        if door and self.doors.is_door_closed(door):
            self.send.private(client, self.door_is_closed_msg(door.name))
            return

        # update the player's current room to the one they're navigating to
        client.player.current_room_id = exit_.id_

        moving_msg = self.moving_msg(client.player.name, exit_.direction.name.lower())

        self.send.private(client, moving_msg.to_self, prompt=False)
        Look(self._telnet, self._world, self._output).process(client, None, [])

        # announce player departure to anyone in the previous room
        self.send.local(current_room.id_, moving_msg.to_room, [client])

        # announce player arrival to anyone in the current room
        self.send.local(
            client.player.current_room_id, moving_msg.to_adjoining_room, [client]
        )
