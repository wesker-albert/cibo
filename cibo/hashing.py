"""Hashing module"""

from passlib.hash import bcrypt


class Password:
    """Contains methods to hash and verify login passwords."""

    # pylint: disable=line-too-long
    def __init__(self):
        self.hasher: bcrypt = bcrypt.using(rounds=13)  # type: ignore[reportGeneralTypeIssues]

    def hash_(self, password_plaintext: str) -> str:
        """Hashes the provided password.

        Args:
            password_plaintext (str): The plaintext password to be hashed

        Returns:
            str: The salted and hashed password.
        """
        return self.hasher.hash(password_plaintext)

    def verify(self, password_plaintext: str, password_hashed: str) -> bool:
        """Verifys the password against a hash.

        Args:
            password_plaintext (str): The plaintext password to be verified
            password_hashed (str): The hashed password to be verified against

        Returns:
            bool: Returns true if password matches the hash
        """
        return self.hasher.verify(password_plaintext, password_hashed)
