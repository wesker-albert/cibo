"""Log in to an existing player on the server."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.actions.commands.look import Look
from cibo.client import Client
from cibo.models.player import Player


class Login(Action):
    """Log in to an existing player on the server."""

    def aliases(self) -> List[str]:
        return ["login"]

    def required_args(self) -> List[str]:
        return ["name", "password"]

    def is_player_logged_in(self, name: str) -> bool:
        """Checks to see if the Player is already logged into and active session, by
        a different client.

        Args:
            name (str): The Player name to check.

        Returns:
            bool: True if the player is already logged in.
        """

        for client in self._telnet.get_connected_clients():
            if client.is_logged_in and client.player and client.player.name == name:
                return True

        return False

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        if client.is_logged_in:
            self.send.private(
                client,
                "You login to Facebook, to make sure your ex isn't doing better "
                "than you are.",
            )
            return

        player_name = args[0]
        password = args[1]

        player = Player.get_by_name(player_name)

        if not player:
            self.send.private(
                client,
                f"A player by the name [cyan]{player_name}[/] does not exist. "
                "If you want, you can [green]register[/] a new player with "
                "that name.",
            )
            return

        # the password the client entered doesn't match the one in the Player record
        if not self._password_hasher.verify(password, player.password):
            self.send.private(client, "[bright_red]Incorrect password.[/]")
            return

        # check to see if another client is already logged in with the Player
        if self.is_player_logged_in(player.name):
            self.send.private(
                client,
                f"The player [cyan]{player_name}[/] is already logged in. "
                "If this player belongs to you and you think it's been stolen, "
                "please contact the admin.",
            )
            return

        client.log_in(player)

        if client.player:
            # join the world and look at the room we left off in
            self.send.private(
                client,
                "You take the [red]red pill[/]. You have a look around, to see how "
                "deep the rabbit hole goes...",
                prompt=False,
            )

            Look(self._telnet, self._world).process(client, None, [])

            # tell everyone we've arrived
            self.send.local(
                client.player.current_room_id,
                f"[cyan]{client.player.name}[/] falls from heaven. It looks like "
                "it hurt.",
                [client],
            )
