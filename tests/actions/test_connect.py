from unittest.mock import ANY, Mock

from cibo.actions.connect import Connect


def test_aliases():
    connect = Connect(Mock(), Mock(), Mock())

    assert not connect.aliases()


def test_required_args():
    connect = Connect(Mock(), Mock(), Mock())

    assert not connect.required_args()


def test_process():
    output = Mock()
    connect = Connect(Mock(), Mock(), output)
    client = Mock()

    connect.process(client, None, [])

    output.private.assert_called_once_with(client, ANY, justify="center")
