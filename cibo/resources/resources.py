"""Resource helper and batch methods that aren't necesarily associated with just one
resource type.
"""

from typing import List, Optional, Union

from cibo.models.item import Item
from cibo.models.npc import Npc


class Resources:
    """Resource helper and batch methods that aren't necesarily associated with just
    one resource type.
    """

    def get_by_name(
        self, resources: List[Union[Item, Npc]], name: str
    ) -> Optional[Union[Item, Npc]]:
        """Finds a resource in a list of resources, with a name that matches or
        contains the provided string. If the string starts with a number followed
        by a period, that number is used as an index assuming there are multiple
        matches.


        Args:
            resources (List[Union[Item, Npc]]): The resources to search against.
            name (str): What to search for in the resource name.

        Returns:
            Optional[Union[Item, Npc]]: The matching resource, if one is found.
        """

        search_name = name
        name_segments = name.split(".")

        # after splitting on periods in the name, if the first character is a number,
        # we want to be able to target that specific index in the resources list
        if name_segments[0].isdigit():
            # a specified index of 0 (zero) returns none -- see the next comment below
            if len(name_segments) > 1 and int(name_segments[0]) > 0:
                search_name = name_segments[1]
            else:
                return None

        results = [resource for resource in resources if search_name in resource.name]

        if not results:
            return None

        if name_segments[0].isdigit():
            try:
                # we expect the initial index to be 1 (not zero) because it's
                # more intuitive from a user perspective, so we have to decrease it
                # here by 1 to be accurate against our list
                return results[(int(name_segments[0]) - 1)]

            except IndexError:
                return None

        return results[0]
