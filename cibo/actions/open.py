"""Open a closed door or object."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.models.door import DoorFlag


class Open(Action):
    """Open a closed door or object."""

    def aliases(self) -> List[str]:
        return ["open"]

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, _command: str, args: List[str]):
        if not client.is_logged_in or not client.player:
            self._send.prompt(client)
            return

        if not args:
            self._send.private(
                client,
                "You open your mouth and let out a loud belch. If anyone else is "
                "in the room, they probably heard it...",
            )
            self._send.local(
                client.player.current_room_id,
                f"[cyan]{client.player.name}[/] burps loudly. How disgusting...",
                [client],
            )
            return

        room = self._world.rooms.get(client.player.current_room_id)

        if room:
            for exit_ in room.exits:
                if args[0] == (exit_.direction.value or exit_.direction.name.lower()):
                    door = self._world.doors.get_by_room_ids(room.id_, exit_.id_)

                    if door:
                        if DoorFlag.LOCKED in door.flags:
                            self._send.private(
                                client, f"The [magenta]{door.name}[/] is locked."
                            )
                            return

                        if not door.flags or DoorFlag.CLOSED in door.flags:
                            door.flags.remove(DoorFlag.CLOSED)
                            door.flags.append(DoorFlag.OPEN)

                            self._send.private(
                                client, f"You open the [magenta]{door.name}[/]."
                            )
                            self._send.local(
                                room.id_,
                                f"[cyan]{client.player.name}[/] opens a "
                                f"[magenta]{door.name}[/].",
                                [client],
                            )
                            self._send.local(
                                exit_.id_, f"A [magenta]{door.name}[/] opens.", [client]
                            )
                            return

                        if DoorFlag.OPEN in door.flags:
                            self._send.private(
                                client, f"The [magenta]{door.name}[/] is already open."
                            )
                            return

            self._send.private(client, "There's nothing to open.")
