"""Navigates a player between available rooms."""

from typing import List

from cibo.actions import Action
from cibo.actions.look import Look
from cibo.client import Client


class Move(Action):
    """Navigates a player between available rooms."""

    def aliases(self) -> List[str]:
        return ["e", "east", "n", "north", "s", "south", "w", "west"]

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, command: str, _args: List[str]):
        if not client.is_logged_in or not client.player:
            self._send.prompt(client)
            return

        room = self._world.rooms.get(client.player.room)

        if room:
            for exit_ in room.exits:
                if command == (exit_.direction.value or exit_.direction.name.lower()):
                    # update the player's current room to the one they're navigating to
                    client.player.room = exit_.id_

                    self._send.private(
                        client,
                        f"You head {exit_.direction.name.lower()}.",
                        prompt=False,
                    )
                    Look(self._telnet, self._world).process(client, None, [])

                    # announce player departure to anyone in the previous room
                    self._send.local(
                        room.id_,
                        f"[cyan]{client.player.name}[/] leaves "
                        f"{exit_.direction.name.lower()}.",
                        [client],
                    )

                    # announce player arrival to anyone in the current room
                    self._send.local(
                        exit_.id_,
                        f"[cyan]{client.player.name}[/] arrives.",
                        [client],
                    )

                    return

            self._send.private(client, "You can't go that way.")
