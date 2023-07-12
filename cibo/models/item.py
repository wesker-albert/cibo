"""An item is an in-game piece of inventory, that can be picked up, carried, and
often used by a player.
"""

from dataclasses import dataclass


@dataclass
class Item:
    """Represents an interactive item."""
