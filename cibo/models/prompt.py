from dataclasses import dataclass

from rich.console import Console


@dataclass
class Prompt:
    body: str
    terminal_width: int = 76

    def _format(self, prompt: str) -> str:
        return f"\r\n{prompt}"

    def __str__(self) -> str:
        formatter = Console(width=self.terminal_width)

        with formatter.capture() as capture:
            formatter.print(self.body, end="", overflow="fold")

        return self._format(capture.get())
