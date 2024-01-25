"""Clients who have disconnected from the server, since last update poll."""


from typing import Any, Optional

from cibo.actions.disconnect import Disconnect
from cibo.events import Event, EventPayload


class DisconnectEvent(Event):
    """Clients who have disconnected from the server, since last update poll."""

    def process(self, _sender: Any, payload: Optional[EventPayload]) -> None:
        if payload:
            Disconnect(self._server_config).process(payload.client, None, [])
