"""Log out of the current player session."""

from typing import List

from cibo.actions import Action
from cibo.client import Client, ClientLoginState


class Logout(Action):
    """Log out of the current player session."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        if not client.is_logged_in or not client.player:
            client.send_prompt()
            return

        player_name = client.player.name

        client.login_state = ClientLoginState.PRE_LOGIN
        client.player = None

        for connected_client in self._telnet.get_connected_clients():
            if connected_client.is_logged_in:
                connected_client.send_message(
                    "A black van pulls up, and 2 large men in labcoats abduct "
                    f"{player_name}. The van speeds away. You wonder if "
                    "you'll ever see your friend again..."
                )

        client.send_message(
            "You slowly fade away into obscurity, like you always feared you would..."
        )

        client.send_message(
            "Welcome to cibo.\n"
            "* Enter 'register name password' to create a new player.\n"
            "* Enter 'login name password' to log in to an existing player."
        )
