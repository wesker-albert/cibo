"""A stylized prompt to be send to the client, and displayed in their terminal.

Leverages the rich library to pad, stylize, and format messages. Accepts
plain strings, or a number of "renderables" that rich offers.

Rich will process a number of color and styling markup codes, if included in
the message.

For more information and to reference ways to use rich in conjunction with
cibo's message formatter, visit:

    https://rich.readthedocs.io/en/stable/
"""

from dataclasses import dataclass

from rich.console import Console


@dataclass
class Prompt:
    """A stylized prompt to be send to the client, and displayed in their terminal."""

    body: str
    terminal_width: int = 76

    def _format(self, prompt: str) -> str:
        return f"\r\n{prompt}"

    def __str__(self) -> str:
        formatter = Console(width=self.terminal_width)

        with formatter.capture() as capture:
            formatter.print(self.body, end="", overflow="fold")

        return self._format(capture.get())
