"""Log in to an existing user on the server."""

from typing import List, Tuple

from cibo.actions import Action
from cibo.actions.commands.look import Look
from cibo.exceptions import (
    ClientIsLoggedIn,
    PasswordIncorrect,
    UserNotFound,
    UserSessionActive,
)
from cibo.models.client import Client
from cibo.models.data.user import User
from cibo.models.message import Message, MessageRoute


class Login(Action):
    """Log in to an existing user on the server."""

    @property
    def aliases(self) -> List[str]:
        return ["login"]

    @property
    def required_args(self) -> List[str]:
        return ["name", "password"]

    @property
    def _is_logged_in_message(self) -> Message:
        """User is already logged in."""

        return Message(
            "You login to Facebook, to make sure your ex isn't doing better than "
            "you are."
        )

    def _user_not_found_message(self, user_name: str) -> Message:
        """User doesn't exist."""

        return Message(
            f"A user by the name [cyan]{user_name}[/] does not exist. "
            "If you want, you can [green]register[/] a new user with that name."
        )

    @property
    def _incorrect_password_message(self) -> Message:
        """Incorrect password entered."""

        return Message("[bright_red]Incorrect password.[/]")

    def _user_session_active_message(self, user_name: str) -> Message:
        """Another client is already logged into a session with the user."""

        return Message(
            f"The user [cyan]{user_name}[/] is already logged in. "
            "If this user belongs to you and you think it's been stolen, please "
            "contact the admin."
        )

    def _logging_in_message(self, user_name: str) -> Tuple[Message, Message]:
        """Successfully loggin in."""

        return (
            Message(
                "You take the [red]red pill[/]. You have a look around, to see how "
                "deep the rabbit hole goes..."
            ),
            Message(f"[cyan]{user_name}[/] falls from heaven. It looks like it hurt."),
        )

    def _check_for_user_session(self, user_name: str) -> None:
        """Checks to see if the user is already logged into an active session, by
        a different client.

        Args:
            user_name (str): The user name to check.

        Raises:
            UserSessionActive: There currently exists an active user session.
        """

        for client in self._telnet.get_connected_clients():
            if client.is_logged_in and client.user.name == user_name:
                raise UserSessionActive

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if client.is_logged_in:
                raise ClientIsLoggedIn

            user_name = args[0]
            password = args[1]

            user = User.get_by_name(user_name)

            self._password_hasher.verify(password, user.password)
            self._check_for_user_session(user.name)

        except ClientIsLoggedIn:
            self.comms.send_to_client(
                MessageRoute(self._is_logged_in_message, client=client)
            )

        except UserNotFound:
            self.comms.send_to_client(
                MessageRoute(self._user_not_found_message(user_name), client=client)
            )

        except PasswordIncorrect:
            self.comms.send_to_client(
                MessageRoute(self._incorrect_password_message, client=client)
            )

        except UserSessionActive:
            self.comms.send_to_client(
                MessageRoute(
                    self._user_session_active_message(user_name), client=client
                )
            )

        else:
            client.log_in(user)

            logging_in_message = self._logging_in_message(client.user.name)

            self.comms.send_to_vicinity(
                MessageRoute(logging_in_message[0], client=client, send_prompt=False),
                MessageRoute(logging_in_message[1], ids=[client.user.current_room_id]),
            )

            Look(self._server_config).process(client, None, [])
