"""Inform the client they have connected to the server."""

from os import getenv
from pathlib import Path
from typing import List, Optional

from rich.panel import Panel

from cibo.actions._base_ import Action
from cibo.models.client import Client
from cibo.models.message import Message, MessageRoute


class Connect(Action):
    """Inform the client they have connected to the server."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    @property
    def _motd_message(self) -> Message:
        return Message(
            Panel(
                f"{self._get_motd()}\n\n"
                "Enter [green]register name password[/] to create a new user.\n"
                "Enter [green]login name password[/] to log in to an existing user.",
                title="Welcome to",
                title_align="left",
                padding=(1, 4),
            ),
            justify="center",
        )

    def _get_motd(self) -> str:
        """Gets an MOTD from a text file, for display when clients connect to the
        server,

        Returns:
            str: The MOTD text.
        """

        motd_path = getenv("MOTD_PATH", "/cibo/config/motd.txt")

        with open(f"{Path.cwd()}{motd_path}", encoding="utf-8") as file:
            motd = file.read()

        return motd

    def process(
        self, client: Client, _command: Optional[str], _args: List[str]
    ) -> None:
        self.comms.send_to_client(MessageRoute(self._motd_message, client=client))
