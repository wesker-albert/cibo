"""Inform the client they have connected to the server."""

from pathlib import Path
from typing import List, Optional

from rich.panel import Panel

from cibo.actions.__action__ import Action
from cibo.client import Client


class Connect(Action):
    """Inform the client they have connected to the server."""

    @property
    def _motd(self) -> str:
        path = Path(__file__).parent.resolve()

        with open(f"{path}/../resources/motd.txt", encoding="utf-8") as file:
            motd = file.read()

        return motd

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, _command: Optional[str], _args: List[str]):
        self._send.private(
            client,
            Panel(
                f"{self._motd}\n\n"
                "Enter [green]register name password[/] to create a new player.\n"
                "Enter [green]login name password[/] to log in to an existing player.",
                title="Welcome to",
                title_align="left",
                padding=(1, 4),
            ),
            justify="center",
        )
