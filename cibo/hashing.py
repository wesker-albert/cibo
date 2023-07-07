from passlib.hash import bcrypt


class Password:
    def __init__(self):
        self.hasher = bcrypt.using(rounds=13)  # type: ignore[reportGeneralTypeIssues]

    def hash_(self, password_plaintext: str) -> str:
        return self.hasher.hash(password_plaintext)

    def verify(self, password_plaintext: str, password_hashed: str) -> bool:
        return self.hasher.verify(password_plaintext, password_hashed)
