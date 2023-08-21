from pytest import raises

from cibo.exception import PlayerNotFound
from cibo.models.data.player import Player


class TestDataPlayer:
    def test_data_player_get_by_name(self):
        player = Player.get_by_name("frank")

        assert player.name == "frank"
        assert player.current_room_id == 1

    def test_data_player_get_by_name_not_found(self):
        with raises(PlayerNotFound):
            _player = Player.get_by_name("mr_nobody")
