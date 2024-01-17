from cibo.models.client import ClientLoginState
from cibo.models.data.user import User
from cibo.models.message import Message, MessageRoute
from tests.actions.conftest import InventoryActionFactory


class TestInventoryAction(InventoryActionFactory):
    def test_action_inventory_aliases(self):
        assert self.inventory.aliases() == ["inventory", "inv", "i"]

    def test_action_inventory_required_args(self):
        assert not self.inventory.required_args()

    def test_action_inventory_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.inventory.process(self.client, "inv", [])

        self.comms.send_prompt.assert_called_once_with(self.client)

    def test_action_inventory_process_empty_inventory(self, _fixture_database):
        self.client.user = User.get_by_name("john")

        self.inventory.process(self.client, "inv", [])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You aren't carrying anything...", **self.default_message_args
                ),
                client=self.client,
            )
        )

    def test_action_inventory_process(self, _fixture_database):
        self.client.user = User.get_by_name("frank")
        self.give_item_to_user(2, self.client.user)

        self.inventory.process(self.client, "inv", [])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(body="A metal fork", **self.default_message_args),
                client=self.client,
            )
        )
