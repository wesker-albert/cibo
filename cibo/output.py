"""The Output class provides message formatting and isolation logic, ensuring
that messages have a uniform style and reach only the clients they are intended to.
"""

from dataclasses import dataclass
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


@dataclass
class Announcement:
    """The information necessary to make a localized announcement."""

    self_message: str
    room_message: str
    adjoining_room_message: Optional[str] = None


class Output:
    """Responsible for constructing messages that are sent to clients.

    Args:
        telnet (TelnetServer): The telnet server to use when outputting messages.
    """

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

        Rich will process a number of color and styling markup codes, if included in
        the message.

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
        """Applies formatting to the prompt text.

        Args:
            prompt (str): The prompt text.

        Returns:
            str: The formatted prompt.
        """

        formatter = Console(width=self._terminal_width)

        with formatter.capture() as capture:
            formatter.print(prompt, end="", overflow="fold")

        return capture.get()

    def send_prompt(self, client: Client) -> None:
        """Prints a formatted prompt to the client.

        Args:
            client (Client): The client to send the prompt to.
        """

        formatted_prompt = self._format_prompt(client.prompt)
        client.send_message(f"\r\n{formatted_prompt}")

    def send_private_message(
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
            self.send_prompt(client)

    def send_local_message(
        self, room_id: int, message: str, ignore_clients: List[Client]
    ) -> None:
        """Prints a message to all clients whose player are within the room.

        Args:
            room_id (int): The room to send the message to.
            message (str): The body of the message.
            ignore_clients (List[Client]): Clients that should not receive the message.
        """

        formatted_message = self._format_message(message)

        for client in self._telnet.get_connected_clients():
            if (
                client.is_logged_in
                and client.player
                and client.player.current_room_id == room_id
                and client not in ignore_clients
            ):
                client.send_message(f"\r{formatted_message}")
                self.send_prompt(client)

    # pylint: disable=too-many-arguments
    def send_local_announcement(
        self,
        announcement: Announcement,
        client: Client,
        room_id: int,
        adjoining_room_id: Optional[int] = None,
        prompt: bool = True,
    ) -> None:
        """Make a localized announcement to the player, other players in the same room,
        and optionally any players in an adjacent room.

        Args:
            announcement (Announcement): The differing messages that will be sent.
            client (Client): The client who is the source of the announcement.
            room_id (int): The originating room of the announcement
            adjoining_room_id (Optional[int], optional): An adjoining room to send a
                message to. Defaults to None.
            prompt (bool, optional): Whether to follow the private client message with
                a prompt. Defaults to True.
        """

        self.send_private_message(client, announcement.self_message, prompt=prompt)
        self.send_local_message(room_id, announcement.room_message, [client])

        if adjoining_room_id and announcement.adjoining_room_message:
            self.send_local_message(
                adjoining_room_id,
                announcement.adjoining_room_message,
                [client],
            )

    def send_sector_announcement(
        self, _sector: int, _message: str, _ignore_clients: List[Client]
    ) -> None:  # pytest: no cover
        """Prints a message to all clients within the sector."""

        pass

    def self_region_announcement(
        self, _region: int, _message: str, _ignore_clients: List[Client]
    ) -> None:  # pytest: no cover
        """Prints a message to all clients within the sector."""

        pass

    def send_server_announcement(
        self, _message: str, _ignore_clients: List[Client]
    ) -> None:  # pytest: no cover
        """Prints a message to all clients on the server."""

        pass
