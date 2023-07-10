"""Commands module"""

from dataclasses import dataclass
from typing import List, Optional, Type

from cibo.action import Action, Finalize, Login, Look, Move, Quit, Register, Say
from cibo.exceptions import CommandMissingArguments, UnrecognizedCommand
from cibo.models.client import Client
from cibo.telnet import TelnetServer


@dataclass
class Command:
    """Maps command alias to the action they should call."""

    aliases: List[str]
    action: Type[Action]


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

    @property
    def _commands(self) -> List[Command]:
        """Commands, their aliases, and the Action class they are mapped to.

        Returns:
            List[CommandAlias]: Commands available to the client
        """

        return [
            Command(
                aliases=["n", "north", "s", "south", "e", "east", "w", "west"],
                action=Move,
            ),
            Command(
                aliases=["look", "l"],
                action=Look,
            ),
            Command(
                aliases=["quit", "leave", "logout"],
                action=Quit,
            ),
            Command(aliases=["login"], action=Login),
            Command(aliases=["register"], action=Register),
            Command(aliases=["finalize"], action=Finalize),
            Command(aliases=["say"], action=Say),
        ]

    def _get_command_action(self, client_command: str) -> Optional[Type[Action]]:
        """Returns the Action for the command identified in the client input, if the
        command alias exists.

        Args:
            _input (str): The client input text

        Returns:
            Optional[Callable]: The action class, if the command is valid
        """
        for mapped_command in self._commands:
            if client_command in mapped_command.aliases:
                return mapped_command.action

        return None

    def execute_action(self, client: Client, input_: str) -> None:
        """Instantiates the Action that is mapped to the command that the client sent
        and then processes the associated logic.

        Args:
            input_ (str): The client input

        Raises:
            UnrecognizedCommand: Raise if the command is unrecognized
        """

        command, _separator, args = input_.partition(" ")
        args = args.split(" ")

        action = self._get_command_action(command)

        if action is None:
            raise UnrecognizedCommand(command)

        action_instance = action(self.telnet)

        try:
            action_instance.process(client, args)

        # and IndexError means that the client's command was missing an argument index
        # that this specific action requires
        except IndexError as ex:
            raise CommandMissingArguments(
                command, action_instance.required_args()
            ) from ex
