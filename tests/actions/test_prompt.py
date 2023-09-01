from tests.conftest import PromptActionFactory


class TestPromptAction(PromptActionFactory):
    def test_action_prompt_aliases(self):
        assert not self.prompt.aliases()

    def test_action_prompt_required_args(self):
        assert not self.prompt.required_args()

    def test_action_prompt_process(self):
        self.prompt.process(self.client, None, [])

        self.output.send_prompt.assert_called_once_with(self.client)
