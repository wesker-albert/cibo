"""Announcements allow us to more easily denote differently formatted messages, that
should then be sent to different recipients depending on things like proximity to
the client that triggered the Action.
"""

from dataclasses import dataclass

# TODO: This shouldn't be a standalone model. It should belong to the Output class,
# likely as a method that appropriately outputs (sends) the given strings without
# further responsibility of the Action calling it.


@dataclass
class Announcement:
    """Houses different formatted strings, that will be sent to different clients."""

    to_self: str
    to_room: str
    to_adjoining_room: str = ""
