from typing import List

from rich.console import Console

from cibo.client import Client


class Prompt:
    def __init__(self) -> None:
        self._terminal_width = 76

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

    def _format(self, prompt: str) -> str:
        return f"\r\n{self._format_prompt(prompt)}"

    def get(self, client: Client) -> List[str]:
        return [self._format(client.prompt)]

    def send(self, client: Client) -> None:
        """Prints a formatted prompt to the client."""

        client.send_message(self.get(client))
