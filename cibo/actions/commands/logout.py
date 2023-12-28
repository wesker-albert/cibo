"""Log out of the current player session."""

from time import sleep
from typing import List

from cibo.actions.__action__ import Action
from cibo.actions.connect import Connect
from cibo.client import Client
from cibo.exception import ClientNotLoggedIn
from cibo.output import Announcement


class Logout(Action):
    """Log out of the current player session."""

    def aliases(self) -> List[str]:
        return ["logout"]

    def required_args(self) -> List[str]:
        return []

    def logging_out_message(self, player_name: str) -> Announcement:
        """Successfully logging the Player out."""

        return Announcement(
            "You slowly fade away into obscurity, like you always feared you would...",
            "A black van pulls up, and 2 large men in labcoats abduct "
            f"[cyan]{player_name}[/]. The van speeds away. You wonder if "
            "you'll ever see them again...",
        )

    def process(
        self, client: Client, command: str, args: List[str], sleep_time: int = 1
    ) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

        except ClientNotLoggedIn:
            self.output.send_prompt(client)

        else:
            player_name = client.player.name
            player_room = client.player.current_room_id

            client.log_out()

            self.output.send_local_announcement(
                self.logging_out_message(player_name), client, player_room, prompt=False
            )

            sleep(sleep_time)

            # process the connection Action, so the client knows they can now register
            # or login again
            Connect(self._server_config).process(client, command, args)
