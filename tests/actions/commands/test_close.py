from tests.conftest import ClientFactory, CloseActionFactory


class TestCloseAction(ClientFactory, CloseActionFactory):
    def test_aliases(self):
        assert self.close.aliases() == ["close"]

    def test_required_args(self):
        assert not self.close.required_args()

    def test_process(self):
        self.close.process(self.mock_client, "close", ["north"])
