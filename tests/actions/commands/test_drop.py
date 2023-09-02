from cibo.client import ClientLoginState
from cibo.models.data.item import Item
from cibo.models.data.player import Player
from cibo.output import Announcement
from tests.conftest import DropActionFactory


class TestDropAction(DropActionFactory):
    def test_action_drop_aliases(self):
        assert self.drop.aliases() == ["drop"]

    def test_action_drop_required_args(self):
        assert not self.drop.required_args()

    def test_action_drop_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.drop.process(self.client, "drop", [])

        self.output.send_prompt.assert_called_once_with(self.client)

    def test_action_drop_process_missing_args(self):
        self.drop.process(self.client, "drop", [])

        self.output.send_private_message.assert_called_with(
            self.client, "Drop what? Your pants? No way!"
        )

    def test_action_drop_process_inventory_item_not_found(self, _fixture_database):
        self.client.player = Player.get_by_name("frank")
        self.give_item_to_player(2, self.client.player)

        self.drop.process(self.client, "drop", ["spoon"])

        self.output.send_private_message.assert_called_with(
            self.client, "You scour your inventory, but can't find that."
        )

    def test_action_drop_process_dropped_tem(self, _fixture_database):
        self.client.player = Player.get_by_name("frank")
        self.give_item_to_player(2, self.client.player)

        self.drop.process(self.client, "drop", ["fork"])

        item = Item.get_by_id(2)

        assert not item.player
        assert item.room_id == 1

        self.output.send_local_announcement.assert_called_once_with(
            Announcement(
                self_message="You drop a metal fork.",
                room_message="[cyan]frank[/] drops a metal fork.",
                adjoining_room_message=None,
            ),
            self.client,
            1,
        )