"""Input sent from clients since the last poll, that needs to be processed by the
CommandProcessor. If the input contains a valid command, further logic will be carried
out."""

from typing import Any, Optional

from cibo.actions.commands._processor_ import CommandProcessor
from cibo.actions.error import Error
from cibo.events import Event, EventPayload
from cibo.exceptions import (
    CommandMissingArguments,
    CommandUnrecognized,
    InputNotReceived,
)
from cibo.server_config import ServerConfig


class InputEvent(Event):
    """Input sent from clients since the last poll, that needs to be processed by the
    CommandProcessor. If the input contains a valid command, further logic will be
    carried out.

    Args:
        server_config (ServerConfig): The server configuration object.
        command_processor (CommandProcessor): The processor to use when evaluating the
            given input.
    """

    def __init__(
        self,
        server_config: ServerConfig,
        signal_name: str,
        command_processor: CommandProcessor,
    ) -> None:
        super().__init__(server_config, signal_name)

        self._command_processor = command_processor

    def process(self, _sender: Any, payload: Optional[EventPayload]) -> None:
        if payload and payload.client:
            try:
                if not payload.input_:
                    raise InputNotReceived

                self._command_processor.process(payload.client, payload.input_)

            except (CommandUnrecognized, CommandMissingArguments) as ex:
                Error(self._server_config).process(payload.client, None, [ex.message])

            except (InputNotReceived, Exception) as ex:
                self._comms.send_prompt(payload.client)

                if not isinstance(ex, InputNotReceived):  # pytest: no cover
                    raise ex
