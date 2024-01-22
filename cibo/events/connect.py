"""Clients who have connected to the server, since last update poll."""

from typing import Any, Optional

from cibo.actions.connect import Connect
from cibo.events import Event, EventPayload


class ConnectEvent(Event):
    """Clients who have connected to the server, since last update poll."""

    def process(self, _sender: Any, payload: Optional[EventPayload]) -> None:
        if payload and payload.client:
            Connect(self._server_config).process(payload.client, None, [])
