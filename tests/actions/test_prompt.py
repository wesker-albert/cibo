from tests.conftest import ClientFactory, PromptActionFactory


class TestPromptAction(ClientFactory, PromptActionFactory):
    def test_aliases(self):
        assert not self.prompt.aliases()

    def test_required_args(self):
        assert not self.prompt.required_args()

    def test_process(self):
        self.prompt.process(self.mock_client, None, [])

        self.output.prompt.assert_called_once_with(self.mock_client)
