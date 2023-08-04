from tests.conftest import ClientFactory, ErrorActionFactory


class TestErrorAction(ClientFactory, ErrorActionFactory):
    def test_action_error_aliases(self):
        assert not self.error.aliases()

    def test_action_error_required_args(self):
        assert self.error.required_args() == ["message"]

    def test_action_error_process(self):
        self.error.process(self.mock_client, None, ["Something unexpected happened!"])

        self.output.private.assert_called_once_with(
            self.mock_client, "[bright_red]Something unexpected happened![/]"
        )
