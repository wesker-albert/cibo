"""Commands module"""

from dataclasses import dataclass
from typing import Callable, List, Optional

from cibo.action import ActionProcessor
from cibo.exceptions import UnrecognizedCommand
from cibo.models.client import Client
from cibo.telnet import TelnetServer


@dataclass
class Command:
    """Maps command alias to the action they should call."""

    aliases: List[str]
    action: Callable


class CommandProcessor:
    """Command processing abstraction layer. Establishes the allowed client commands and
    command aliases, and maps them to action methods.
    """

    def __init__(self, telnet: TelnetServer) -> None:
        """Creates the command processor instance.

        Args:
            telnet (TelnetServer):  The Telnet server to use when executing the action
        """

        self.telnet = telnet
        self._action_processor = ActionProcessor(self.telnet)

    @property
    def _directional_aliases(self) -> List[str]:
        """Aliases for directional navigation.

        Returns:
            List[str]: Directional navigation aliases
        """

        return ["n", "north", "s", "south", "e", "east", "w", "west"]

    @property
    def _commands(self) -> List[Command]:
        """Commands, their aliases, and the action methods the are mapped to.

        Returns:
            List[CommandAlias]: Commands available to the client
        """

        return [
            Command(
                aliases=self._directional_aliases, action=self._action_processor.move
            ),
            Command(aliases=["look", "l"], action=self._action_processor.look),
            Command(
                aliases=["quit", "exit", "leave", "logout"],
                action=self._action_processor.quit_,
            ),
            Command(aliases=["login"], action=self._action_processor.login),
            Command(aliases=["register"], action=self._action_processor.register),
            Command(aliases=["say"], action=self._action_processor.say),
        ]

    def _get_command_action(self, client_command: str) -> Optional[Callable]:
        """Returns the action for the command identified in the client input, if the
        command alias exists.

        Args:
            _input (str): The client input text

        Returns:
            Optional[Callable]: The action method, if the command is valid
        """
        for mapped_command in self._commands:
            if client_command in mapped_command.aliases:
                return mapped_command.action

        return None

    def execute_action(self, client: Client, input_: str) -> None:
        """Calls the action that is mapped to the command that the client sent.

        Args:
            input_ (str): The client input

        Raises:
            UnrecognizedCommand: Raise if the command is unrecognized
        """

        command, _separator, args = input_.partition(" ")

        action = self._get_command_action(command)

        if action is None:
            raise UnrecognizedCommand(command)

        action(client, args)
