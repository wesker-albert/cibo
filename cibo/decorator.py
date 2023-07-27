"""Decorators that are useful to bootstrap class methods."""

from functools import wraps
from typing import Any, Callable

from dotenv import load_dotenv


def load_environment_variables(function: Callable) -> Callable:
    """Decorator that loads the environment variables contained within the `.env` file
    before calling the wrapped function.
    """

    @wraps(function)
    def wrapper(*args: tuple, **kwargs: dict) -> Any:
        load_dotenv()
        return function(*args, **kwargs)

    return wrapper
