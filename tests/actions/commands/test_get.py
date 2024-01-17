from cibo.models.client import ClientLoginState
from cibo.models.data.item import Item
from cibo.models.data.user import User
from cibo.models.message import Message, MessageRoute
from tests.actions.conftest import GetActionFactory


class TestGetAction(GetActionFactory):
    def test_action_get_aliases(self):
        assert self.get.aliases() == ["get"]

    def test_action_get_required_args(self):
        assert not self.get.required_args()

    def test_action_get_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.get.process(self.client, "get", [])

        self.comms.send_prompt.assert_called_once_with(self.client)

    def test_action_get_process_missing_args(self):
        self.get.process(self.client, "get", [])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You don't get it, and you probably never will.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_get_process_room_item_not_found(self, _fixture_database):
        self.client.user = User.get_by_name("frank")

        self.get.process(self.client, "get", ["spoon"])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You look around, but don't see that.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_get_process_item_is_stationary(self, _fixture_database):
        self.client.user = User.get_by_name("frank")

        self.get.process(self.client, "get", ["jukebox"])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You try, but you can't take that.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_get_process_dropped_tem(self, _fixture_database):
        self.client.user = User.get_by_name("frank")

        self.get.process(self.client, "get", ["fork"])

        item = Item.get_by_id(1)

        assert item.user == self.client.user
        assert not item.current_room_id

        self.comms.send_to_vicinity.assert_called_once_with(
            MessageRoute(
                Message(body="You pick up a metal fork.", **self.default_message_args),
                client=self.client,
            ),
            MessageRoute(
                Message(
                    body="[cyan]frank[/] picks up a metal fork.",
                    **self.default_message_args,
                ),
                ids=[1],
            ),
        )
