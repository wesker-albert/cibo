from dataclasses import dataclass
from typing import Literal, Optional, Union

from rich.columns import Columns
from rich.console import Console
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree


@dataclass
class Message:
    """A message.

    Args:
        message (Union[str, Columns, Markdown, Panel, Syntax, Table, Tree]):
            The message or rich renderable to format.
        justify (Optional[Literal["left", "center", "right"]], optional):
            Alignment of the message contents. Defaults to None.
        style (Optional[str], optional): A style to apply to the whole message.
            Defaults to None.
        highlight (bool, optional): Highlight patterns in text, such as int, str,
            etc. Defaults to False.
    """

    body: Union[str, Columns, Markdown, Panel, Syntax, Table, Tree]
    justify: Optional[Literal["left", "center", "right"]] = None
    style: Optional[str] = None
    highlight: bool = False
    terminal_width: int = 76

    def __str__(self) -> str:
        """Leverages the rich library to pad, stylize, and format messages. Accepts
        plain strings, or a number of "renderables" that rich offers.

        Rich will process a number of color and styling markup codes, if included in
        the message.

        For more information and to reference ways to use rich in conjunction with
        cibo's message formatter, visit:

            https://rich.readthedocs.io/en/stable/

        Returns:
            str: The padded and formatted message.
        """

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
    room_id: int
    message: Message
