"""A stylized message to be send to the client, and displayed in their terminal.

Leverages the rich library to pad, stylize, and format messages. Accepts
plain strings, or a number of "renderables" that rich offers.

Rich will process a number of color and styling markup codes, if included in
the message.

For more information and to reference ways to use rich in conjunction with
cibo's message formatter, visit:

    https://rich.readthedocs.io/en/stable/
"""

from dataclasses import KW_ONLY, dataclass, field
from typing import List, Literal, Optional, Union

from rich.columns import Columns
from rich.console import Console
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

from cibo.models.client import Client


@dataclass
class Message:
    """A stylized message to be send to the client, and displayed in their terminal."""

    body: Union[str, Columns, Markdown, Panel, Syntax, Table, Tree]
    _: KW_ONLY
    justify: Optional[Literal["left", "center", "right"]] = None
    style: Optional[str] = None
    highlight: bool = False
    terminal_width: int = 76

    def __str__(self) -> str:
        formatter = Console(
            width=self.terminal_width, style=self.style, highlight=self.highlight
        )

        with formatter.capture() as capture:
            padded_message = Padding(self.body, (0, 2))
            formatter.print(
                padded_message, end="", overflow="fold", justify=self.justify
            )

        return capture.get()


@dataclass
class MessageRoute:
    """Used to associate a message with specific clients, rooms, sectors, or regions,
    for routing and delivery purposes.
    """

    message: Message
    _: KW_ONLY
    client: Optional[Client] = None
    ignored_clients: List[Client] = field(default_factory=lambda: [])
    ids: List[int] = field(default_factory=lambda: [])
    send_prompt: bool = True
