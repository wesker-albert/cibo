from pytest import raises

from cibo.exceptions import UserNotFound
from cibo.models.data.user import User
from tests.conftest import DatabaseFactory


class TestDataUser(DatabaseFactory):
    def test_data_user_get_by_name(self, _fixture_database):
        user = User.get_by_name("frank")

        assert user.name == "frank"
        assert user.current_room_id == 1

    def test_data_user_get_by_name_not_found(self, _fixture_database):
        with raises(UserNotFound):
            _user = User.get_by_name("mr_nobody")
