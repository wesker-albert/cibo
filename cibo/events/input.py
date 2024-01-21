"""Input sent from clients since the last poll, that needs to be processed by the
CommandProcessor. If the input contains a valid command, further logic will be carried
out."""

from typing import Any

from cibo.actions.commands._processor_ import CommandProcessor
from cibo.actions.error import Error
from cibo.events._base_ import Event
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
        command_processor: CommandProcessor,
    ) -> None:
        super().__init__(server_config)

        self._command_processor = command_processor

        self._process.connect(self.process)

    def process(self, _sender: Any) -> None:
        for client, input_ in self._telnet.get_client_input():
            try:
                if not input_:
                    raise InputNotReceived

                self._command_processor.process(client, input_)

            except (CommandUnrecognized, CommandMissingArguments) as ex:
                Error(self._server_config).process(client, None, [ex.message])

            except (InputNotReceived, Exception) as ex:
                self._comms.send_prompt(client)

                if not isinstance(ex, InputNotReceived):  # pytest: no cover
                    raise ex
