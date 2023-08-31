from tests.conftest import ErrorActionFactory


class TestErrorAction(ErrorActionFactory):
    def test_action_error_aliases(self):
        assert not self.error.aliases()

    def test_action_error_required_args(self):
        assert self.error.required_args() == ["message"]

    def test_action_error_process(self):
        self.error.process(self.client, None, ["Something unexpected happened!"])

        self.output.send_private_message.assert_called_once_with(
            self.client, "[bright_red]Something unexpected happened![/]"
        )
