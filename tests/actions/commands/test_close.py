from tests.conftest import ClientFactory, CloseActionFactory


class TestCloseAction(ClientFactory, CloseActionFactory):
    def test_action_close_aliases(self):
        assert self.close.aliases() == ["close"]

    def test_action_close_required_args(self):
        assert not self.close.required_args()

    def test_action_close_process(self):
        self.close.process(self.mock_client, "close", ["north"])
