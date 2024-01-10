from tests.actions.conftest import EverySecondActionFactory


class TestEverySecondAction(EverySecondActionFactory):
    def test_action_every_second_aliases(self):
        assert not self.every_second.aliases()

    def test_action_every_second_required_args(self):
        assert not self.every_second.required_args()

    def test_action_every_second_process(self):
        self.every_second.process(self.client, None, [])
