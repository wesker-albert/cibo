"""Inform the client they have connected to the server."""

from typing import List, Optional

from rich.panel import Panel

from cibo.actions.__action__ import Action
from cibo.models.client import Client
from cibo.models.message import Message


class Connect(Action):
    """Inform the client they have connected to the server."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    @property
    def motd_message(self) -> Message:
        return Message(
            Panel(
                f"{self._world.motd}\n\n"
                "Enter [green]register name password[/] to create a new player.\n"
                "Enter [green]login name password[/] to log in to an existing player.",
                title="Welcome to",
                title_align="left",
                padding=(1, 4),
            ),
            justify="center",
        )

    def process(
        self, client: Client, _command: Optional[str], _args: List[str]
    ) -> None:
        self.output.send_private_message(client, self.motd_message)
