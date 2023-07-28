from unittest.mock import Mock

from cibo.actions.prompt import Prompt


def test_aliases():
    prompt = Prompt(Mock(), Mock(), Mock())

    assert not prompt.aliases()


def test_required_args():
    prompt = Prompt(Mock(), Mock(), Mock())

    assert not prompt.required_args()


def test_process():
    output = Mock()
    prompt = Prompt(Mock(), Mock(), output)
    client = Mock()

    prompt.process(client, None, [])

    output.prompt.assert_called_once_with(client)
