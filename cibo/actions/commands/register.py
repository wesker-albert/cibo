"""Register a new user with the server."""

from typing import List

from marshmallow import ValidationError

from cibo.actions import Action
from cibo.exceptions import ClientIsLoggedIn, UserAlreadyExists, UserNotFound
from cibo.models.client import Client
from cibo.models.data.user import User, UserSchema
from cibo.models.message import Message, MessageRoute


class Register(Action):
    """Register a new user with the server."""

    @property
    def aliases(self) -> List[str]:
        return ["register"]

    @property
    def required_args(self) -> List[str]:
        return ["name", "password"]

    @property
    def _is_logged_in_message(self) -> Message:
        """User is already logged in."""

        return Message(
            "You register to vote, even though both candidates aren't that great."
        )

    @property
    def _validation_error_message(self) -> Message:
        """Provided registration info is invalid."""

        return Message(
            "[bright_red]Your user name or password don't meet criteria.[/]\n\n"
            "Names must be 3-15 chars and only contain letters, numbers, or "
            "underscores. They are case-sensitive.\n\n"
            "Passwords must be minimum 8 chars.\n\n"
            "Please [green]register[/] again."
        )

    def _user_already_exists_message(self, user_name: str) -> Message:
        """User name is already taken."""

        return Message(
            f"Sorry, turns out the name [cyan]{user_name}[/] is already taken. "
            "Please [green]register[/] again with a different name."
        )

    def _confirm_finalize_message(self, user_name: str) -> Message:
        """Ask the client to finalize the user registration."""

        return Message(
            "Are you sure you want to create the user named "
            f"[cyan]{user_name}[/]?\n\n"
            "Type [green]finalize[/] to finalize the user creation. "
            "If you want to use a different name or password, you can "
            "[green]register[/] again.\n\n"
            "Otherwise, feel free to [green]login[/] to an already "
            "existing user."
        )

    def _validate_user_info(self, name: str, password: str) -> None:
        """Validates the supplied user information, to see if it follows the
        requirements established by the schema.

        Args:
            name (str): The user name to validate.
            password (str): The password to validate.
        """

        User(name=name, password=password).validate(UserSchema)

    def _check_for_existing_user(self, user_name: str) -> None:
        """Checks to see if a user already exists witht the provided name.

        Args:
            user_name (str): The name to check against.

        Raises:
            UserAlreadyExists: A user with that name exists.
        """

        _existing_user = User.get_by_name(user_name)

        raise UserAlreadyExists

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if client.is_logged_in:
                raise ClientIsLoggedIn

            user_name = args[0]
            password = args[1]

            self._validate_user_info(user_name, password)
            self._check_for_existing_user(user_name)

        except ClientIsLoggedIn:
            self.comms.send_to_client(
                MessageRoute(self._is_logged_in_message, client=client)
            )

        except UserAlreadyExists:
            self.comms.send_to_client(
                MessageRoute(
                    self._user_already_exists_message(user_name), client=client
                )
            )

        except ValidationError:
            self.comms.send_to_client(
                MessageRoute(self._validation_error_message, client=client)
            )

        except UserNotFound:
            # a temporary User model is set on the client, to be created in the db if
            # they call the Finalize action
            client.registration = User(
                name=user_name,
                password=self._password_hasher.hash_(password),
                current_room_id=1,
            )

            self.comms.send_to_client(
                MessageRoute(self._confirm_finalize_message(user_name), client=client)
            )
