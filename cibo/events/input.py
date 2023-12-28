"""Input send from clients since the last poll, that needs to be processed by the
CommandProcessor. If the input contains a valid Command, further logic will be carried
out."""

from cibo.actions.error import Error
from cibo.actions.prompt import Prompt
from cibo.command import CommandProcessor
from cibo.config import ServerConfig
from cibo.events.__event__ import Event
from cibo.exception import (
    CommandMissingArguments,
    CommandUnrecognized,
    InputNotReceived,
)


class InputEvent(Event):
    """Input sent from clients since the last poll, that needs to be processed by the
    CommandProcessor. If the input contains a valid Command, further logic will be
    carried out.
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
                Prompt(self._server_config).process(client, None, [])

                if not isinstance(ex, InputNotReceived):  # pytest: no cover
                    raise ex
