"""Close an open door or object."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.models.door import DoorFlag


class Close(Action):
    """Close an open door or object."""

    def aliases(self) -> List[str]:
        return ["close"]

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, _command: str, args: List[str]):
        if not client.is_logged_in or not client.player:
            self._send.prompt(client)
            return

        if not args:
            self._send.private(
                client,
                "You close your eyes and daydream about money and success.",
            )
            return

        room = self._world.rooms.get(client.player.current_room_id)

        if room:
            for exit_ in room.exits:
                if args[0] == (exit_.direction.value or exit_.direction.name.lower()):
                    door = self._world.doors.get_by_room_ids(room.id_, exit_.id_)

                    if door:
                        if (
                            not door.flags
                            or DoorFlag.CLOSED in door.flags
                            or DoorFlag.LOCKED in door.flags
                        ):
                            self._send.private(
                                client,
                                f"The [magenta]{door.name}[/] is already closed.",
                            )
                            return

                        if DoorFlag.OPEN in door.flags:
                            door.flags.remove(DoorFlag.OPEN)
                            door.flags.append(DoorFlag.CLOSED)

                            self._send.private(
                                client, f"You close the [magenta]{door.name}[/]."
                            )
                            self._send.local(
                                room.id_,
                                f"[cyan]{client.player.name}[/] closes a "
                                f"[magenta]{door.name}[/].",
                                [client],
                            )
                            self._send.local(
                                exit_.id_,
                                f"A [magenta]{door.name}[/] closes.",
                                [client],
                            )
                            return

            self._send.private(client, "There's nothing to close.")
