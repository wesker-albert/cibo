import json
from dataclasses import dataclass

from cibo.models.terminal import TerminalColors, TerminalStyle


@dataclass
class Messages:
    """Formatted messages that are available for output to a client"""

    prompt: str

    def __init__(self, filename: str) -> dict:
        super().__init__()

        self._color = TerminalColors()
        self._style = TerminalStyle()
        self._json_data = self._load_json_data(filename)

        self.prompt = self._json_data["prompt"]

    def __post_init__(self):
        # TODO: iterate over instance properties and replace color/style placeholders
        # with correlating enum values
        return

    def _load_json_data(self, filename) -> dict:
        with open(filename, encoding="utf-8") as file:
            json_data: dict = json.load(file)

        return json_data
