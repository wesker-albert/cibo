from unittest.mock import Mock

from cibo.actions.prompt import Prompt
from cibo.client import Client


def test_aliases():
    prompt = Prompt(Mock(), Mock(), Mock())

    assert not prompt.aliases()


def test_required_args():
    prompt = Prompt(Mock(), Mock(), Mock())

    assert not prompt.required_args()


def test_process(client: Client):
    output = Mock()
    output.prompt = Mock()
    prompt = Prompt(Mock(), Mock(), output)

    prompt.process(client, None, [])

    output.prompt.assert_called_once_with(client)
