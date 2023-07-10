"""Exceptions module"""


class UnrecognizedCommand(Exception):
    """Raised if the client's command is unrecognized."""

    def __init__(self, command: str):
        self.message = f"Unrecognized command: {command}"
