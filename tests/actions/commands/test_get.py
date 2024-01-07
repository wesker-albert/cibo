from cibo.models.client import ClientLoginState
from cibo.models.data.item import Item
from cibo.models.data.player import Player
from cibo.outputs import Announcement
from tests.conftest import GetActionFactory


class TestGetAction(GetActionFactory):
    def test_action_get_aliases(self):
        assert self.get.aliases() == ["get"]

    def test_action_get_required_args(self):
        assert not self.get.required_args()

    def test_action_get_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.get.process(self.client, "get", [])

        self.output.send_prompt.assert_called_once_with(self.client)

    def test_action_get_process_missing_args(self):
        self.get.process(self.client, "get", [])

        self.output.send_to_client.assert_called_with(
            self.client, "You don't get it, and you probably never will."
        )

    def test_action_get_process_room_item_not_found(self, _fixture_database):
        self.client.player = Player.get_by_name("frank")

        self.get.process(self.client, "get", ["spoon"])

        self.output.send_to_client.assert_called_with(
            self.client, "You look around, but don't see that."
        )

    def test_action_get_process_item_is_stationary(self, _fixture_database):
        self.client.player = Player.get_by_name("frank")

        self.get.process(self.client, "get", ["jukebox"])

        self.output.send_to_client.assert_called_with(
            self.client, "You try, but you can't take that."
        )

    def test_action_get_process_dropped_tem(self, _fixture_database):
        self.client.player = Player.get_by_name("frank")

        self.get.process(self.client, "get", ["fork"])

        item = Item.get_by_id(1)

        assert item.player == self.client.player
        assert not item.current_room_id

        self.output.send_local_announcement.assert_called_once_with(
            Announcement(
                self_message="You pick up a metal fork.",
                room_message="[cyan]frank[/] picks up a metal fork.",
                adjoining_room_message=None,
            ),
            self.client,
            1,
        )
