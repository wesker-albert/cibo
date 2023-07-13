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
        return ["name", "password"]

    def process(self, client: Client, args: List[str]):
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
                f"Sorry, turns out the name #MAGENTA#{player_name}#NOCOLOR# is already "
                "taken. Please #GREEN#register#NOCOLOR# again with a different name.",
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
                f"#MAGENTA#{player_name}#NOCOLOR#?",
                prompt=False,
            )
            self._send.private(
                client,
                "Type #GREEN#finalize#NOCOLOR# to finalize the player creation. "
                "If you want to use a different name or password, you can "
                "#GREEN#register#NOCOLOR# again.",
                prompt=False,
            )
            self._send.private(
                client,
                "Otherwise, feel free to #GREEN#login#NOCOLOR# to an already "
                "existing player.",
            )

        # schema validation failed for the Player model
        except ValidationError:
            self._send.private(
                client,
                "#LRED#Your player name or password don't meet criteria.#NOCOLOR#",
                prompt=False,
            )
            self._send.private(
                client,
                "Names must be 3-15 chars and only contain letters, numbers, or "
                "underscores.",
                prompt=False,
            )
            self._send.private(
                client,
                "Passwords must be minimum 8 chars.",
                newline=False,
                prompt=False,
            )
            self._send.private(client, "Please #GREEN#register#NOCOLOR# again.")
