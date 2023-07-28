from unittest.mock import Mock

from cibo.actions.error import Error


def test_aliases():
    error = Error(Mock(), Mock(), Mock())

    assert not error.aliases()


def test_required_args():
    error = Error(Mock(), Mock(), Mock())

    assert error.required_args() == ["message"]


def test_process():
    output = Mock()
    error = Error(Mock(), Mock(), output)
    client = Mock()

    error.process(client, None, ["Something unexpected happened!"])

    output.private.assert_called_once_with(
        client, "[bright_red]Something unexpected happened![/]"
    )
