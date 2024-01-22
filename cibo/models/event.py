"""Event models are used by signal-driven events, to help establish reliable payload
structure and protocols.
"""

from dataclasses import dataclass
from typing import Optional

from cibo.models.client import Client


@dataclass
class EventPayload:
    """A payload that supplies the event with any data it may need."""

    client: Optional[Client] = None
    input_: Optional[str] = None
