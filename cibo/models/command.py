"""Models relating to client commands and input."""

from dataclasses import dataclass
from typing import Any, List


@dataclass
class CommandHistoryEntry:
    """Represents a previously inputted command, sent to the server by a client."""

    command: str
    args: List[str]


@dataclass
class CommandFlowState:
    target_action: type[Any]
    state_slug: str
    expected_responses: List[str]
