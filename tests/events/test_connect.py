from unittest.mock import Mock

from cibo.client import Client
from cibo.events.connect import ConnectEvent


def test_process(client: Client):
    telnet = Mock()
    telnet.get_new_clients.return_value = [client]

    output = Mock()

    connect = ConnectEvent(telnet, Mock(), output)

    connect.process()

    output.private.assert_called_once()
