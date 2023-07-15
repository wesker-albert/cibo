"""The Output class provides message formatting and isolation logic, ensuring
that messages have a uniform style and reach only the clients they are intended to.
"""

from typing import List, Literal, Optional, Union

from rich.columns import Columns
from rich.console import Console
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

from cibo.client import Client
from cibo.telnet import TelnetServer


class Output:
    """Responsible for constructing messages that are sent to clients."""

    def __init__(self, telnet: TelnetServer) -> None:
        self._telnet = telnet
        self._terminal_width = 76

    def _format_message(
        self,
        message: Union[str, Columns, Markdown, Panel, Syntax, Table, Tree],
        justify: Optional[Literal["left", "center", "right"]] = None,
        style: Optional[str] = None,
        highlight: bool = False,
    ) -> str:
        """Leverages the rich library to pad, stylize, and format messages. Accepts
        plain strings, or a number of "renderables" that rich offers.

        Rich will process a number of color and styling markup codes.

        For more information and to reference ways to use rich in conjunction with
        cibo's message formatter, visit:

            https://rich.readthedocs.io/en/stable/

        Args:
            message (Union[str, Columns, Markdown, Panel, Syntax, Table, Tree]):
                The message or rich renderable to format.
            justify (Optional[Literal["left", "center", "right"]], optional):
                Alignment of the message contents. Defaults to None.
            style (Optional[str], optional): A style to apply to the whole message.
                Defaults to None.
            highlight (bool, optional): Highlight patterns in text, such as int, str,
                etc. Defaults to False.

        Returns:
            str: The padded and formatted message.
        """

        formatter = Console(
            width=self._terminal_width, style=style, highlight=highlight
        )

        with formatter.capture() as capture:
            padded_message = Padding(message, (0, 2))
            formatter.print(padded_message, end="", overflow="fold", justify=justify)

        return capture.get()

    def _format_prompt(self, prompt: str) -> str:
        """_summary_

        Args:
            prompt (str): The prompt text.

        Returns:
            str: The formatted prompt.
        """

        formatter = Console(width=self._terminal_width)

        with formatter.capture() as capture:
            formatter.print(prompt, end="", overflow="fold")

        return capture.get()

    def prompt(self, client: Client) -> None:
        """Prints a formatted prompt to the client.

        Args:
            client (Client): The client to send the prompt to.
        """

        formatted_prompt = self._format_prompt(client.prompt)
        client.send_message(f"\r\n{formatted_prompt}")

    def private(
        self,
        client: Client,
        message: Union[str, Columns, Markdown, Panel, Syntax, Table, Tree],
        justify: Optional[Literal["left", "center", "right"]] = None,
        prompt: bool = True,
    ) -> None:
        """Prints a message only to the client specified.

        Args:
            client (Client): The client to send the message to.
            message (Union[str, Columns, Markdown, Panel, Syntax, Table, Tree]):
                The message or rich renderable to format.
            justify (Optional[Literal["left", "center", "right"]], optional):
                Alignment of the message contents. Defaults to None.
            prompt (bool, optional): If a prompt should be included immediately after
                the message. Defaults to True.
        """

        formatted_message = self._format_message(message, justify=justify)
        client.send_message(f"\n{formatted_message}")

        if prompt:
            self.prompt(client)

    # TODO: when we implement the concept of "rooms", make this method only send to
    # the clients in the room specified
    def local(self, message: str, ignore_clients: List[Client]) -> None:
        """Prints a message to all clients whose plater are within the room.

        Args:
            message (str): The body of the message
            ignore_clients (List[Client]): Clients that should not receive the message
        """

        formatted_message = self._format_message(message)

        for client in self._telnet.get_connected_clients():
            if client.is_logged_in and client not in ignore_clients:
                client.send_message(f"\r{formatted_message}")
                self.prompt(client)

    def sector(
        self, _sector: int, _message: str, _ignore_clients: List[Client]
    ) -> None:
        """Prints a message to all clients within the sector."""

        pass

    def region(
        self, _region: int, _message: str, _ignore_clients: List[Client]
    ) -> None:
        """Prints a message to all clients within the sector."""

        pass

    def server(self, _message: str, _ignore_clients: List[Client]) -> None:
        """Prints a message to all clients on the server."""

        pass
