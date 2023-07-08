"""Terminal color and style models"""

from enum import Enum


class TerminalColors(str, Enum):
    """Codes to display color in terminal output."""

    BLACK = "\033[30m"
    RED = "\033[31m"
    LIGHT_RED = "\033[91m"
    GREEN = "\033[32m"
    LIGHT_GREEN = "\033[92m"
    YELLOW = "\033[33m"
    LIGHT_YELLOW = "\033[93m"
    BLUE = "\033[34m"
    LIGHT_BLUE = "\033[94m"
    MAGENTA = "\033[35m"
    LIGHT_MAGENTA = "\033[95m"
    CYAN = "\033[36m"
    LIGHTCYAN = "\033[96m"
    GRAY = "\033[37m"
    DARK_GRAY = "\033[90m"
    WHITE = "\033[97m"
    NO_COLOR = "\033[0m\033[49m"


class TerminalStyle(str, Enum):
    """Codes to display text styles in terminal output."""

    BOLD = "\033[1m"
    NO_STYLE = "\033[22m"
