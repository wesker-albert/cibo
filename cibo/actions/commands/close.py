"""Close an open door or object."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client


class Close(Action):
    """Close an open door or object."""

    def aliases(self) -> List[str]:
        return ["close"]

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, _command: str, args: List[str]):
        if not client.is_logged_in:
            self.send.prompt(client)
            return

        if not args:
            self.send.private(
                client,
                "You close your eyes and daydream about money and success.",
            )
            return

        room = self.rooms.get_by_id(client.player.current_room_id)
        exit_ = self.rooms.get_direction_exit(room, args[0])

        if not exit_:
            self.send.private(client, "There's nothing to close.")
            return

        door = self.doors.get_by_room_ids(room.id_, exit_.id_)

        if self.doors.is_door_closed(door):
            self.send.private(
                client,
                f"The [magenta]{door.name}[/] is already closed.",
            )
            return

        if self.doors.is_door_open(door):
            self.doors.close_door(door)

            self.send.private(client, f"You close the [magenta]{door.name}[/].")
            self.send.local(
                room.id_,
                f"[cyan]{client.player.name}[/] closes a " f"[magenta]{door.name}[/].",
                [client],
            )
            self.send.local(
                exit_.id_,
                f"A [magenta]{door.name}[/] closes.",
                [client],
            )
