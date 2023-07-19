"""Log in to an existing player on the server."""

from typing import List

from peewee import DoesNotExist

from cibo.actions.__action__ import Action
from cibo.actions.commands.look import Look
from cibo.client import Client, ClientLoginState
from cibo.models.player import Player


class Login(Action):
    """Log in to an existing player on the server."""

    def aliases(self) -> List[str]:
        return ["login"]

    def required_args(self) -> List[str]:
        return ["name", "password"]

    def process(self, client: Client, _command: str, args: List[str]):
        if client.is_logged_in:
            self._send.private(
                client,
                "You login to Facebook, to make sure your ex isn't doing better "
                "than you are.",
            )
            return

        player_name = args[0]
        password = args[1]

        try:
            existing_player = Player.get(Player.name == player_name)

        # a Player doesn't exist with the entered name
        except DoesNotExist:
            self._send.private(
                client,
                f"A player by the name [cyan]{player_name}[/] does not exist. "
                "If you want, you can [green]register[/] a new player with "
                "that name.",
            )
            return

        # the password the client entered doesn't match the one in the Player entry
        if not self._password_hasher.verify(password, existing_player.password):
            self._send.private(client, "[bright_red]Incorrect password.[/]")
            return

        # check to see if another client is already logged in with the Player
        for connected_client in self._telnet.get_connected_clients():
            if (
                connected_client.is_logged_in
                and connected_client.player
                and connected_client.player.name == player_name
            ):
                self._send.private(
                    client,
                    f"The player [cyan]{player_name}[/] is already logged in. "
                    "If this player belongs to you and you think it's been stolen, "
                    "please contact the admin.",
                )
                return

        client.player = existing_player
        client.login_state = ClientLoginState.LOGGED_IN

        # join the world and look at the room we left off in
        self._send.private(
            client,
            "You take the [red]red pill[/]. You have a look around, to see how deep "
            "the rabbit hole goes...",
            prompt=False,
        )

        Look(self._telnet, self._world).process(client, None, [])

        # tell everyone we've arrived
        self._send.local(
            client.player.current_room_id,
            f"[cyan]{client.player.name}[/] falls from heaven. It looks like "
            "it hurt.",
            [client],
        )
