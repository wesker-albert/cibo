"""An Npc is a non-player character, that a player might encounter while exploring
the world. Some Npcs can be interacted with, in varying ways.

This is a collection of all the Npcs that exist in the world.
"""

from typing import List

from cibo.exception import NpcNotFound
from cibo.models.npc import Npc, NpcDescription
from cibo.resources.__resource__ import Resource


class Npcs(Resource):
    """All the Npcs that exist in the world."""

    def __init__(self, npcs_file: str):
        self._npcs: List[Npc] = self._generate_resources(npcs_file)

    def _create_resource_from_dict(self, resource: dict) -> Npc:
        npc = resource

        return Npc(
            id_=npc["id"],
            name=npc["name"],
            description=NpcDescription(
                room=npc["description"]["room"], look=npc["description"]["look"]
            ),
        )

    def get_by_id(self, id_: int) -> Npc:
        """Get an Npc by it's ID.

        Args:
            id_ (int): The Npc ID you're looking for.

        Raises:
            NpcNotFound: The Npc does not exist in the World.

        Returns:
            Npc: The matched Npc.
        """

        for npc in self._npcs:
            if npc.id_ == id_:
                return npc

        raise NpcNotFound
