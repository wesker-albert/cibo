"""Register a new player with the server."""

from typing import List

from marshmallow import ValidationError
from peewee import DoesNotExist

from cibo.actions import Action
from cibo.client import Client
from cibo.models import Player, PlayerSchema


class Register(Action):
    """Register a new player with the server."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return ["name", "password"]

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        if client.is_logged_in:
            client.send_message(
                "You register to vote, even though both candidates aren't that great."
            )
            return

        player_name = args[0]
        password = args[1]

        # verify a Player with the same name doesn't already exist
        try:
            _existing_player = Player.get(Player.name == player_name)

            client.send_message(
                f"Sorry, turns out the name '{player_name}' is already "
                "taken.\n"
                "Please 'register' again with a different name."
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

            client.send_message(
                f"Are you sure you want to create the player named '{player_name}'?\n"
                "* Type 'finalize' to finalize the player creation.\n"
                "* If you want to use a different name or password, you can 'register' "
                "again.\n"
                "* Otherwise, feel free to 'login' to an already existing player."
            )

        # schema validation failed for the Player model
        except ValidationError:
            client.send_message(
                "Your player name or password don't meet criteria:\n"
                "* Names must be 3-15 chars and only contain letters, numbers, or "
                "underscores.\n"
                "* Passwords must be minimum 8 chars.\n"
                "Please 'register' again."
            )
