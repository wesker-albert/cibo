"""Inform the client they have connected to the server."""

from typing import List

from cibo.actions import Action
from cibo.client import Client


class _Connect(Action):
    """Inform the client they have connected to the server."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, args: List[str]):
        self._send.private(client, "#BLUE#Welcome to cibo.#NOCOLOR#", prompt=False)
        self._send.private(
            client,
            "Enter #GREEN#register name password#NOCOLOR# to create a new player.",
            newline=False,
            prompt=False,
        )
        self._send.private(
            client,
            "Enter #GREEN#login name password#NOCOLOR# to log in to an existing "
            "player.",
            newline=False,
        )
