from pytest import fixture, raises

from cibo.exception import PasswordIncorrect
from cibo.password import Password


class TestPassword:
    @fixture(autouse=True)
    def fixture_hasher(self):
        self.hasher = Password()

    def test_password_verify(self):
        hashed_password = self.hasher.hash_("abc123")

        self.hasher.verify("abc123", hashed_password)

    def test_password_verify_failure(self):
        hashed_password = self.hasher.hash_("abc123")

        with raises(PasswordIncorrect):
            self.hasher.verify("def456", hashed_password)
