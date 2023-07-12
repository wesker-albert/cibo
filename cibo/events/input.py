from cibo.command import CommandProcessor
from cibo.events import Event
from cibo.exception import CommandMissingArguments, UnrecognizedCommand
from cibo.telnet import TelnetServer


class Input(Event):
    """Incoming client input Event. Kicks off the Command processor, to process
    the input.
    """

    def __init__(
        self, telnet: TelnetServer, command_processor: CommandProcessor
    ) -> None:
        super().__init__(telnet)

        self._command_processor = command_processor

    def process(self) -> None:
        """Process incoming client input."""

        for client, input_ in self._telnet.get_client_input():
            if input_:
                try:
                    self._command_processor.process(client, input_)

                except (
                    UnrecognizedCommand,
                    CommandMissingArguments,
                ) as ex:
                    client.send_message(ex.message)
