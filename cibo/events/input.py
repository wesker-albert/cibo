"""Input send from clients since the last poll, that needs to be processed by the
CommandProcessor. If the input contains a valid Command, further logic will be carried
out."""

from cibo.actions.error import Error
from cibo.actions.prompt import Prompt
from cibo.command import CommandProcessor
from cibo.events.__event__ import Event
from cibo.exception import CommandMissingArguments, UnrecognizedCommand
from cibo.resources.world import World
from cibo.telnet import TelnetServer


class InputEvent(Event):
    """Input send from clients since the last poll, that needs to be processed by the
    CommandProcessor. If the input contains a valid Command, further logic will be
    carried out.
    """

    def __init__(self, telnet: TelnetServer, world: World) -> None:
        super().__init__(telnet, world)

        self._command_processor = CommandProcessor(self._telnet, self._world)

    def process(self) -> None:
        for client, input_ in self._telnet.get_client_input():
            if not input_:
                Prompt(self._telnet, self._world).process(client, None, [])
                return

            try:
                self._command_processor.process(client, input_)

            except (
                UnrecognizedCommand,
                CommandMissingArguments,
            ) as ex:
                Error(self._telnet, self._world).process(client, None, [ex.message])
