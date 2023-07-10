"""Exceptions module"""


from typing import List


class UnrecognizedCommand(Exception):
    """Raised if the client's command is unrecognized."""

    def __init__(self, command: str):
        self.message = f"Unrecognized command: {command}"


class CommandMissingArguments(Exception):
    """Raised if the client's command is missing expected arguments."""

    def __init__(self, command: str, required_args: List[str]):
        joined_args = " ".join([str(x) for x in required_args])

        self.message = (
            "Command is missing required arguments. "
            f"Expected syntax: {command} {joined_args}"
        )
