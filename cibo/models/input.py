"""Models relating to client input and commands."""

from dataclasses import dataclass
from typing import List


@dataclass
class InputHistoryEntry:
    """Represents a previously inputted command, sent to the server by a client."""

    command: str
    args: List[str]
