"""Navigates a player between available rooms."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.actions.commands.look import Look
from cibo.client import Client
from cibo.exception import ResourceNotFound


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

    def process(self, client: Client, command: str, _args: List[str]) -> None:
        if not client.is_logged_in or not client.player:
            self.send.prompt(client)
            return

        try:
            current_room = self.rooms.get_by_id(client.player.current_room_id)
            exit_ = self.rooms.get_direction_exit(current_room, command)

            if not exit_:
                self.send.private(client, "You can't go that way.")
                return

            door = self.doors.get_by_room_ids(current_room.id_, exit_.id_)

            if self.doors.is_door_closed(door):
                self.send.private(client, f"The [magenta]{door.name}[/] is closed.")
                return

            # update the player's current room to the one they're navigating to
            client.player.current_room_id = exit_.id_

            self.send.private(
                client,
                f"You head {exit_.direction.name.lower()}.",
                prompt=False,
            )
            Look(self._telnet, self._world, self._output).process(client, None, [])

            # announce player departure to anyone in the previous room
            self.send.local(
                current_room.id_,
                f"[cyan]{client.player.name}[/] leaves "
                f"{exit_.direction.name.lower()}.",
                [client],
            )

            # announce player arrival to anyone in the current room
            self.send.local(
                client.player.current_room_id,
                f"[cyan]{client.player.name}[/] arrives.",
                [client],
            )

        except ResourceNotFound:
            self.send.prompt(client)
            return
