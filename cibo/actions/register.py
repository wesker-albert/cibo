"""Register a new player with the server."""

from typing import List

from marshmallow import ValidationError
from peewee import DoesNotExist

from cibo.actions import Action
from cibo.client import Client
from cibo.models import Player, PlayerSchema


class Register(Action):
    """Register a new player with the server."""

    def aliases(self) -> List[str]:
        return ["register"]

    def required_args(self) -> List[str]:
        return ["name", "password"]

    def process(self, client: Client, _command: str, args: List[str]):
        if client.is_logged_in:
            self._send.private(
                client,
                "You register to vote, even though both candidates aren't that great.",
            )
            return

        player_name = args[0]
        password = args[1]

        # verify a Player with the same name doesn't already exist
        try:
            _existing_player = Player.get(Player.name == player_name)

            self._send.private(
                client,
                f"Sorry, turns out the name [magenta]{player_name}[/] is already "
                "taken. Please [green]register[/] again with a different name.",
            )
            return

        except DoesNotExist:
            pass

        try:
            Player(name=player_name, password=password).validate(PlayerSchema)

            # a temporary Player model is set on the client, to be created in the db if
            # they call the Finalize action
            client.registration = Player(
                name=player_name, password=self._password_hasher.hash_(password)
            )

            self._send.private(
                client,
                "Are you sure you want to create the player named "
                f"[magenta]{player_name}[/]?\n\n"
                "Type [green]finalize[/] to finalize the player creation. "
                "If you want to use a different name or password, you can "
                "[green]register[/] again.\n\n"
                "Otherwise, feel free to [green]login[/] to an already "
                "existing player.",
            )

        # schema validation failed for the Player model
        except ValidationError:
            self._send.private(
                client,
                "[bright_red]Your player name or password don't meet criteria.[/]\n\n"
                "Names must be 3-15 chars and only contain letters, numbers, or "
                "underscores. They are case-sensitive.\n\n"
                "Passwords must be minimum 8 chars.\n\n"
                "Please [green]register[/] again.",
            )
