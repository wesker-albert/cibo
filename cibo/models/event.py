from dataclasses import dataclass
from typing import Optional

from cibo.models.client import Client


@dataclass
class EventPayload:
    """A payload that supplies the event with any data it may need."""

    client: Optional[Client] = None
    input_: Optional[str] = None
