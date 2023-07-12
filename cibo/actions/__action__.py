"""Abstraction to be used as a base class for every Action."""

from abc import ABC, abstractmethod
from typing import List

from cibo.client import Client
from cibo.password import Password
from cibo.telnet import TelnetServer


class Action(ABC):
    """The base interface used by all Action classes."""

    def __init__(self, telnet: TelnetServer) -> None:
        self._telnet = telnet
        self._password_hasher = Password()

    def _join_args(self, args: List[str]) -> str:
        """Join the list of args into a singular string, using a space as the
        delimiter.

        Args:
            args (List[str]): The list of args

        Returns:
            str: All the args as one big string
        """

        return " ".join([str(x) for x in args])

    @abstractmethod
    def required_args(self) -> List[str]:
        """Descriptions of the args required for the Action. If no arguments are
        necessary for the Action, return an empty list.

        Returns:
            List[str]: Descriptions for each required argument
        """

        pass

    @abstractmethod
    def process(self, client: Client, args: List[str]) -> None:
        """Process the logic for the Action.

        Args:
            client (Client): The client who triggered the Action
            args (List[str]): The args included with the command maped to the Action
        """

        pass
