"""Commands are specific strings of input a client can send to the server, that
will in turn trigger the Action mapped to that Command.
"""

from dataclasses import dataclass
from typing import List, Optional, Type

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.config import ServerConfig
from cibo.exception import CommandMissingArguments, CommandUnrecognized


@dataclass
class Command:
    """Maps command aliases to the action they should call."""

    aliases: List[str]
    action: Type[Action]


class CommandProcessor:
    """Command processing abstraction layer. Establishes the allowed client commands and
    command aliases, and maps them to action methods.

    Args:
        server_config (ServerConfig): The server configuration object.
        actions (List[type[Action]]): The Action classes available to the processor.
    """

    def __init__(
        self,
        server_config: ServerConfig,
        actions: List[type[Action]],
    ) -> None:
        self._server_config = server_config
        self._actions = actions

    @property
    def _commands(self) -> List[Command]:
        """Commands, their aliases, and the Action class they are mapped to.

        Returns:
            List[Command]: Commands available to the client.
        """

        return [
            Command(
                aliases=action(self._server_config).aliases(),
                action=action,
            )
            for action in self._actions
        ]

    def _get_command_action(self, client_command: str) -> Optional[Type[Action]]:
        """Returns the Action for the command identified in the client input, if the
        command alias exists.

        Args:
            client_command (str): The command the client sent.

        Returns:
            Optional[Type[Action]]: The action class, if the command is valid.
        """

        for mapped_command in self._commands:
            # we convert aliases to lowercase, to avoid case sensitivity
            if client_command in [alias.lower() for alias in mapped_command.aliases]:
                return mapped_command.action

        return None

    def process(self, client: Client, input_: str) -> None:
        """Instantiates the Action that is mapped to the command that the client sent
        and then processes the associated logic.

        Args:
            client (Client): The client who sent the command input.
            input_ (str): The client command and args.

        Raises:
            CommandUnrecognized: The client command is unrecognized.
            CommandMissingArguments: The client command is missing required args.
        """

        # separate the command from the args, then also split each of the individual
        # args into a list
        command, _separator, args = input_.partition(" ")
        # convert the command to lowercase, to avoid case sensitivity
        command = command.lower()
        # partition returns a blank string if no args are found after the command
        # in that case, we want to drop the blank string and just return an empty list
        split_args = args.split(" ") if args else []

        action = self._get_command_action(command)

        if action is None:
            raise CommandUnrecognized(command)

        action_instance = action(self._server_config)

        try:
            action_instance.process(client, command, split_args)

        # an IndexError means that the client's command was missing an argument index
        # that this specific action requires
        except IndexError as ex:
            raise CommandMissingArguments(
                command, action_instance.required_args()
            ) from ex
