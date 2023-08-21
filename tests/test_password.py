from pytest import raises

from cibo.exception import PasswordIncorrect
from tests.conftest import PasswordFactory


class TestPassword(PasswordFactory):
    def test_password_verify(self):
        self.password.verify("abc123", self.hashed_password)

    def test_password_verify_failure(self):
        with raises(PasswordIncorrect):
            self.password.verify("def456", self.hashed_password)
