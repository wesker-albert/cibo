from cibo.client import ClientLoginState
from cibo.models.data.player import Player
from tests.conftest import InventoryActionFactory


class TestInventoryAction(InventoryActionFactory):
    def test_action_inventory_aliases(self):
        assert self.inventory.aliases() == ["inventory", "inv", "i"]

    def test_action_inventory_required_args(self):
        assert not self.inventory.required_args()

    def test_action_inventory_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.inventory.process(self.client, "inv", [])

        self.output.send_prompt.assert_called_once_with(self.client)

    def test_action_inventory_process_empty_inventory(self, _fixture_database):
        self.client.player = Player.get_by_name("john")

        self.inventory.process(self.client, "inv", [])

        self.output.send_private_message.assert_called_with(
            self.client, "You aren't carrying anything..."
        )

    def test_action_inventory_process(self, _fixture_database):
        self.client.player = Player.get_by_name("frank")
        self.give_item_to_player(2, self.client.player)

        self.inventory.process(self.client, "inv", [])

        self.output.send_private_message.assert_called_with(self.client, "A metal fork")
