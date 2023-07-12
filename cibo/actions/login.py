"""Log in to an existing player on the server."""

from typing import List

from peewee import DoesNotExist

from cibo.actions import Action
from cibo.client import Client, ClientLoginState
from cibo.models import Player


class Login(Action):
    """Log in to an existing player on the server."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return ["name", "password"]

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        if client.is_logged_in:
            client.send_message(
                "You login to Facebook, to make sure your ex isn't doing better "
                "than you are."
            )
            return

        player_name = args[0]
        password = args[1]

        try:
            existing_player = Player.get(Player.name == player_name)

        # a Player doesn't exist with the entered name
        except DoesNotExist:
            client.send_message(
                f"A player by the name '{player_name}' does not exist.\n"
                "If you want, you can 'register' a new player with that name."
            )
            return

        # the password the client entered doesn't match the one in the Player entry
        if not self._password_hasher.verify(password, existing_player.password):
            client.send_message("Incorrect password.")
            return

        # check to see if another client is already logged in with the Player
        for connected_client in self._telnet.get_connected_clients():
            if (
                connected_client.is_logged_in
                and connected_client.player
                and connected_client.player.name == player_name
            ):
                client.send_message(
                    f"The player '{player_name}' is already logged in. If this "
                    "player belongs to you and you think it's been stolen, please "
                    "contact the admin."
                )
                return

        client.player = existing_player
        client.login_state = ClientLoginState.LOGGED_IN

        client.send_message(
            "You awaken from a pleasant dream, and find yourself amongst friends."
        )
