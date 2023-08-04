"""An item is an in-game piece of inventory, that can be picked up, carried, and
often used by a player.
"""

from dataclasses import dataclass


@dataclass  # pytest: no cover
class Item:  # pytest: no cover
    """Represents an interactive item."""
