from cibo.models import ClientLoginState, Message, MessageRoute
from cibo.models.data import Item, Player
from tests.actions.conftest import DropActionFactory


class TestDropAction(DropActionFactory):
    def test_action_drop_aliases(self):
        assert self.drop.aliases() == ["drop"]

    def test_action_drop_required_args(self):
        assert not self.drop.required_args()

    def test_action_drop_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.drop.process(self.client, "drop", [])

        self.comms.send_prompt.assert_called_once_with(self.client)

    def test_action_drop_process_missing_args(self):
        self.drop.process(self.client, "drop", [])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="Drop what? Your pants? No way!",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_drop_process_inventory_item_not_found(self, _fixture_database):
        self.client.player = Player.get_by_name("frank")
        self.give_item_to_player(2, self.client.player)

        self.drop.process(self.client, "drop", ["spoon"])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You scour your inventory, but can't find that.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_drop_process_dropped_tem(self, _fixture_database):
        self.client.player = Player.get_by_name("frank")
        self.give_item_to_player(2, self.client.player)

        self.drop.process(self.client, "drop", ["fork"])

        item = Item.get_by_id(2)

        assert not item.player
        assert item.current_room_id == 1

        self.comms.send_to_vicinity.assert_called_once_with(
            MessageRoute(
                Message(body="You drop a metal fork.", **self.default_message_args),
                client=self.client,
            ),
            MessageRoute(
                Message(
                    body="[cyan]frank[/] drops a metal fork.",
                    **self.default_message_args,
                ),
                ids=[1],
            ),
        )
