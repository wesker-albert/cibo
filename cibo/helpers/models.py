"""Model helpers"""

from marshmallow import validate


def field_is_alphanumeric():
    """Validates the model field is alphanumeric."""

    return validate.Regexp(
        "^[a-zA-Z0-9_]*$", error="Can only contain numbers, letters, or underscores."
    )
