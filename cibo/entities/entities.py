"""Entity helper and batch methods that aren't necesarily associated with just one
entity type.
"""

from typing import List, Optional, Union

from cibo.models.item import Item
from cibo.models.npc import Npc


class Entities:
    """Entity helper and batch methods that aren't necesarily associated with just
    one entity type.
    """

    def get_by_name(
        self, entities: List[Union[Item, Npc]], sub: str
    ) -> Optional[Union[Item, Npc]]:
        """Finds a entity in a list of entities, with a name that matches or
        contains the provided substring. If the substring starts with a number
        followed by a period, that number is used as an index assuming there are
        multiple matches.

        Args:
            entities (List[Union[Item, Npc]]): The entities to search against.
            sub (str): What to search for in the entity name.

        Returns:
            Optional[Union[Item, Npc]]: The matching entity, if one is found.
        """

        _sub = sub
        sub_segments = sub.split(".")

        # after splitting on periods in the substring, if the first character is a
        # number, we want to be able to target that specific index in the entities
        # list
        if sub_segments[0].isdigit():
            # a specified index of 0 (zero) returns None -- see the next comment below
            if len(sub_segments) > 1 and int(sub_segments[0]) > 0:
                _sub = sub_segments[1]
            else:
                return None

        results = [entity for entity in entities if _sub in entity.name]

        if not results:
            return None

        if sub_segments[0].isdigit():
            try:
                # we expect the initial index to be 1 (not zero) because it's
                # more intuitive from a user perspective, so we have to decrease it
                # here by 1 to be accurate against our list
                return results[(int(sub_segments[0]) - 1)]

            except IndexError:
                return None

        return results[0]