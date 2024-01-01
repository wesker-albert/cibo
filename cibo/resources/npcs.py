"""An NPC is a non-player character, that a player might encounter while exploring
the world. Some NPCs can be interacted with, in varying ways.

This is a collection of all the NPCs that exist in the world.
"""

from typing import List

from cibo.exception import NpcNotFound
from cibo.models.data.npc import Npc as NpcData
from cibo.models.description import EntityDescription
from cibo.models.npc import Npc
from cibo.resources.__resource__ import Composite, Resource


class Npcs(Resource):
    """All the NPCs that exist in the world."""

    def __init__(self, npcs_file: str):
        self._npcs: List[Npc] = self._generate_resources(npcs_file)
        self.get_by_name = Composite().get_by_name

    def _create_resource_from_dict(self, resource: dict) -> Npc:
        npc = resource

        return Npc(
            id_=npc["id"],
            name=npc["name"],
            description=EntityDescription(
                room=npc["description"]["room"],
                look=npc["description"]["look"],
            ),
        )

    def get_by_id(self, id_: int) -> Npc:
        """Get an NPC by it's ID.

        Args:
            id_ (int): The NPC ID you're looking for.

        Raises:
            NpcNotFound: The NPC does not exist in the world.

        Returns:
            Npc: The matched NPC.
        """

        for npc in self._npcs:
            if npc.id_ == id_:
                return npc

        raise NpcNotFound

    def get_from_dataset(self, npcs_dataset: List[NpcData]) -> List[Npc]:
        """Compiles a list of NPCs, using the IDS from a set of corresponding
        NPC data models.

        Args:
            npcs_dataset (List[NpcData]): The set of NPC data models.

        Returns:
            List[Npc]: The compiled list of NPCs.
        """

        return [self.get_by_id(npc.npc_id) for npc in npcs_dataset]
