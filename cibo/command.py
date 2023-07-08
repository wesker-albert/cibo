"""Commands module"""

from cibo.action import Action


class Command(Action):
    """Aliases mapped to actions, available for client execution."""

    @property
    def directional_aliases(self):
        """Aliases for directional navigation."""
        directions = {
            "north": ("n", "north"),
            "south": ("s", "south"),
            "east": ("e", "east"),
            "west": ("w", "west"),
        }

        return tuple(item for sublist in directions.values() for item in sublist)

    @property
    def aliases(self):
        """Aliases mapped to specific Actions."""
        return {
            "move": {"aliases": self.directional_aliases, "command": self.move},
            "look": {"aliases": ("l", "look"), "command": self.look},
            "quit": {
                "aliases": ("exit", "quit", "leave", "logout"),
                "command": self.quit_,
            },
        }

    def is_valid_command(self, input_: str) -> bool:
        """Validates user input against existing aliases."""
        for _key, value in self.aliases.items():
            if " " in input_ and input_[: input_.index(" ")] in value["aliases"]:
                return True

            if input_ in value["aliases"]:
                return True

        return False
