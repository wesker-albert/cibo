"""Input sent from clients since the last poll, that needs to be processed by the
CommandProcessor. If the input contains a valid command, further logic will be carried
out."""

from cibo.actions.error import Error
from cibo.command import CommandProcessor
from cibo.events.__event__ import Event
from cibo.exception import (
    CommandMissingArguments,
    CommandUnrecognized,
    InputNotReceived,
)
from cibo.models.server_config import ServerConfig


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

    def process(self) -> None:
        for client, input_ in self._telnet.get_client_input():
            try:
                if not input_:
                    raise InputNotReceived

                self._command_processor.process(client, input_)

            except (CommandUnrecognized, CommandMissingArguments) as ex:
                Error(self._server_config).process(client, None, [ex.message])

            except (InputNotReceived, Exception) as ex:
                client.send_prompt()

                if not isinstance(ex, InputNotReceived):  # pytest: no cover
                    raise ex
