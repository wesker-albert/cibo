"""Input send from clients since the last poll, that needs to be processed by the
CommandProcessor. If the input contains a valid Command, further logic will be carried
out."""

from cibo.actions import _Error
from cibo.command import CommandProcessor
from cibo.events import Event
from cibo.exception import CommandMissingArguments, UnrecognizedCommand
from cibo.telnet import TelnetServer


class Input(Event):
    """Input send from clients since the last poll, that needs to be processed by the
    CommandProcessor. If the input contains a valid Command, further logic will be
    carried out.
    """

    def __init__(
        self, telnet: TelnetServer, command_processor: CommandProcessor
    ) -> None:
        super().__init__(telnet)

        self._command_processor = command_processor

    def process(self) -> None:
        for client, input_ in self._telnet.get_client_input():
            if input_:
                try:
                    self._command_processor.process(client, input_)

                except (
                    UnrecognizedCommand,
                    CommandMissingArguments,
                ) as ex:
                    _Error(self._telnet).process(client, None, [ex.message])
