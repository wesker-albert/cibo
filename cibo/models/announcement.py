"""Announcements allow us to more easily denote differently formatted messages, that
should then be sent to different recipients depending on things like proximity to
the client that triggered the Action.
"""

from dataclasses import dataclass


@dataclass
class Announcement:
    """Houses different formatted strings, that will be sent to different clients."""

    to_self: str
    to_room: str
    to_adjoining_room: str = ""
