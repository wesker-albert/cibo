"""Navigates a player between available rooms."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.actions.look import Look
from cibo.client import Client


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

    def process(self, client: Client, command: str, _args: List[str]):
        if not client.is_logged_in or not client.player:
            self._send.prompt(client)
            return

        previous_room = self._world.rooms.get(client.player.current_room_id)

        if previous_room:
            for exit_ in previous_room.exits:
                if command == (exit_.direction.value or exit_.direction.name.lower()):
                    # update the player's current room to the one they're navigating to
                    client.player.current_room_id = exit_.id_

                    self._send.private(
                        client,
                        f"You head {exit_.direction.name.lower()}.",
                        prompt=False,
                    )
                    Look(self._telnet, self._world).process(client, None, [])

                    # announce player departure to anyone in the previous room
                    self._send.local(
                        previous_room.id_,
                        f"[cyan]{client.player.name}[/] leaves "
                        f"{exit_.direction.name.lower()}.",
                        [client],
                    )

                    # announce player arrival to anyone in the current room
                    self._send.local(
                        client.player.current_room_id,
                        f"[cyan]{client.player.name}[/] arrives.",
                        [client],
                    )

                    return

            self._send.private(client, "You can't go that way.")
