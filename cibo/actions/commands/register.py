"""Register a new player with the server."""

from typing import List

from marshmallow import ValidationError

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import ClientIsLoggedIn, PlayerAlreadyExists, PlayerNotFound
from cibo.models.data.player import Player, PlayerSchema


class Register(Action):
    """Register a new player with the server."""

    def aliases(self) -> List[str]:
        return ["register"]

    def required_args(self) -> List[str]:
        return ["name", "password"]

    @property
    def is_logged_in_message(self) -> str:
        """Player is already logged in."""

        return "You register to vote, even though both candidates aren't that great."

    def player_already_exists_message(self, player_name: str) -> str:
        """Player name is already taken."""

        return (
            f"Sorry, turns out the name [cyan]{player_name}[/] is already taken. "
            "Please [green]register[/] again with a different name."
        )

    @property
    def validation_error_message(self) -> str:
        """Provided registration info is invalid."""

        return (
            "[bright_red]Your player name or password don't meet criteria.[/]\n\n"
            "Names must be 3-15 chars and only contain letters, numbers, or "
            "underscores. They are case-sensitive.\n\n"
            "Passwords must be minimum 8 chars.\n\n"
            "Please [green]register[/] again."
        )

    def confirm_finalize_message(self, player_name: str) -> str:
        """Ask the client to finalize the player registration."""

        return (
            "Are you sure you want to create the player named "
            f"[cyan]{player_name}[/]?\n\n"
            "Type [green]finalize[/] to finalize the player creation. "
            "If you want to use a different name or password, you can "
            "[green]register[/] again.\n\n"
            "Otherwise, feel free to [green]login[/] to an already "
            "existing player."
        )

    def validate_player_info(self, name: str, password: str) -> None:
        """Validates the supplied player information, to see if it follows the
        requirements established by the schema.

        Args:
            name (str): The player name to validate.
            password (str): The password to validate.
        """

        Player(name=name, password=password).validate(PlayerSchema)

    def check_for_existing_player(self, player_name: str) -> None:
        """Checks to see if a player already exists witht the provided name.

        Args:
            player_name (str): The name to check against.

        Raises:
            PlayerAlreadyExists: A player with that name exists.
        """

        _existing_player = Player.get_by_name(player_name)

        raise PlayerAlreadyExists

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if client.is_logged_in:
                raise ClientIsLoggedIn

            player_name = args[0]
            password = args[1]

            self.validate_player_info(player_name, password)
            self.check_for_existing_player(player_name)

        except ClientIsLoggedIn:
            self.output.send_private_message(client, self.is_logged_in_message)

        except PlayerAlreadyExists:
            self.output.send_private_message(
                client, self.player_already_exists_message(player_name)
            )

        except ValidationError:
            self.output.send_private_message(client, self.validation_error_message)

        except PlayerNotFound:
            # a temporary Player model is set on the client, to be created in the db if
            # they call the Finalize action
            client.registration = Player(
                name=player_name,
                password=self._password_hasher.hash_(password),
                current_room_id=1,
            )

            self.output.send_private_message(
                client, self.confirm_finalize_message(player_name)
            )
