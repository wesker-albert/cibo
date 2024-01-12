"""Provides password hashing and verification."""

from passlib.hash import bcrypt

from cibo.exceptions import PasswordIncorrect


class Password:
    """Contains methods to hash and verify login passwords."""

    def __init__(self) -> None:
        self._bcrypt: bcrypt = bcrypt.using(rounds=13)

    def hash_(self, password_plaintext: str) -> str:
        """Hashes the provided password.

        Args:
            password_plaintext (str): The plaintext password to be hashed.

        Returns:
            str: The salted and hashed password.
        """

        return str(self._bcrypt.hash(password_plaintext))

    def verify(self, password_plaintext: str, password_hashed: str) -> None:
        """Verifies the password against a hash.

        Args:
            password_plaintext (str): The plaintext password to be verified.
            password_hashed (str): The hashed password to be verified against.

        Returns:
            bool: Returns true if password matches the hash.
        """

        is_valid = bool(self._bcrypt.verify(password_plaintext, password_hashed))

        if not is_valid:
            raise PasswordIncorrect
