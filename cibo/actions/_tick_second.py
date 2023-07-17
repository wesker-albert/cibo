"""Repetative logic that is carried out every second."""

from typing import List, Optional

from cibo.actions.__action__ import Action
from cibo.client import Client


class _TickSecond(Action):
    """Repetative logic that is carried out every second."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(self, _client: Client, _command: Optional[str], _args: List[str]):
        pass
