"""Log out of the current player session."""

from typing import List

from cibo.actions import Action, _Connect
from cibo.client import Client, ClientLoginState


class Logout(Action):
    """Log out of the current player session."""

    def aliases(self) -> List[str]:
        return ["logout"]

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, args: List[str]):
        if not client.is_logged_in or not client.player:
            self._send.prompt(client)
            return

        player_name = client.player.name

        client.login_state = ClientLoginState.PRE_LOGIN
        client.player = None

        self._send.local(
            "A black van pulls up, and 2 large men in labcoats abduct "
            f"[magenta]{player_name}[/]. The van speeds away. You wonder if "
            "you'll ever see your friend again...",
            [client],
        )

        self._send.private(
            client,
            "You slowly fade away into obscurity, like you always feared you would...",
            prompt=False,
        )

        # process the connection Action, so the client knows they can now register
        # or login again
        _Connect(self._telnet).process(client, [])
