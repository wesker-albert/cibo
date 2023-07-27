"""Register a new player with the server."""

from typing import List

from marshmallow import ValidationError

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.models.player import Player, PlayerSchema


class Register(Action):
    """Register a new player with the server."""

    def aliases(self) -> List[str]:
        return ["register"]

    def required_args(self) -> List[str]:
        return ["name", "password"]

    def is_registration_valid(self, name: str, password: str) -> bool:
        """Validates the supplied Player information, to see if it follows the
        requirements established by the schema.

        Args:
            name (str): The Player name to validate.
            password (str): The password to validate.

        Returns:
            bool: True if the validation was successful.
        """

        try:
            Player(name=name, password=password).validate(PlayerSchema)

            return True

        except ValidationError:
            return False

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        if client.is_logged_in:
            self.send.private(
                client,
                "You register to vote, even though both candidates aren't that great.",
            )
            return

        player_name = args[0]
        password = args[1]

        # verify a Player with the same name doesn't already exist
        existing_player = Player.get_by_name(player_name)

        if existing_player:
            self.send.private(
                client,
                f"Sorry, the name [cyan]{player_name}[/] is already taken. "
                "Please [green]register[/] again with a different name.",
            )
            return

        if not self.is_registration_valid(player_name, password):
            self.send.private(
                client,
                "[bright_red]Your player name or password don't meet criteria.[/]\n\n"
                "Names must be 3-15 chars and only contain letters, numbers, or "
                "underscores. They are case-sensitive.\n\n"
                "Passwords must be minimum 8 chars.\n\n"
                "Please [green]register[/] again.",
            )
            return

        # a temporary Player model is set on the client, to be created in the db if
        # they call the Finalize action
        client.registration = Player(
            name=player_name,
            password=self._password_hasher.hash_(password),
            current_room_id=1,
        )

        self.send.private(
            client,
            "Are you sure you want to create the player named "
            f"[cyan]{player_name}[/]?\n\n"
            "Type [green]finalize[/] to finalize the player creation. "
            "If you want to use a different name or password, you can "
            "[green]register[/] again.\n\n"
            "Otherwise, feel free to [green]login[/] to an already "
            "existing player.",
        )
