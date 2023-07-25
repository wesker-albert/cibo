"""Inform the client they have connected to the server."""

from typing import List, Optional

from rich.panel import Panel

from cibo.actions.__action__ import Action
from cibo.client import Client


class Connect(Action):
    """Inform the client they have connected to the server."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, _command: Optional[str], _args: List[str]):
        self.send.private(
            client,
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
