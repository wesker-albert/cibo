from dataclasses import dataclass


@dataclass
class EntityDescription:
    """Descriptions of an Npc or Item, depending on context."""

    room: str
    look: str
