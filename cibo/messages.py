"""Messages module"""

import json
from dataclasses import dataclass
from pathlib import Path

from cibo.models.terminal import TerminalColors, TerminalStyle

# TODO: I would favor loading static message strings from the db rather than a JSON file
# so this is likely a temporary module providing convience during early development


@dataclass
class Messages:
    """Formatted messages that are available for output to a client"""

    prompt: str

    def __init__(self, filename: str):
        super().__init__()

        self.color = TerminalColors
        self.style = TerminalStyle
        self.json_data = self.__load_json_data(filename)

        self.prompt = self.json_data["prompt"]

    def __post_init__(self):
        # TODO: iterate over instance properties and replace color/style placeholders
        # with correlating enum values
        return

    def __load_json_data(self, filename) -> dict:
        path = Path(__file__).parent.resolve()

        with open(f"{path}/../{filename}", encoding="utf-8") as file:
            json_data = json.load(file)

        return json_data
