"""Event models are used by signal-driven events, to help establish reliable payload
structure and protocols.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from cibo.models.client import Client


class EventType(str, Enum):
    """The kinds of events that can be dispatched and subscribed to."""

    CONNECT = "event-connect"
    DISCONNECT = "event-disconnect"
    INPUT = "event-input"
    TICK = "event-tick"
    SPAWN = "event-spawn"

    def __str__(self) -> str:
        return self.value


@dataclass
class EventPayload:
    """A payload that supplies the event with any data it may need."""

    client: Client
    input_: Optional[str] = None
