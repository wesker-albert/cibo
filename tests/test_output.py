from unittest.mock import Mock, call

from cibo.client import Client, ClientLoginState
from cibo.output import Output


def test_prompt(output: Output, mock_client: Client):
    output.prompt(mock_client)

    mock_client.send_message.assert_called_once_with("\r\n> ")


def test_private(output: Output, mock_client: Client):
    output.private(mock_client, "You are tired.")

    calls = [
        call(
            "\n  You are tired.                                                            \n"
        ),
        call("\r\n> "),
    ]

    mock_client.send_message.assert_has_calls(calls)


def test_private_no_prompt(output: Output, mock_client: Client):
    output.private(mock_client, "You are tired.", prompt=False)

    mock_client.send_message.assert_called_once_with(
        "\n  You are tired.                                                            \n"
    )


def test_local(mock_client: Client):
    telnet = Mock()
    output = Output(telnet)

    mock_client.login_state = ClientLoginState.LOGGED_IN
    mock_client.player = Mock(current_room_id=1)

    telnet.get_connected_clients.return_value = [mock_client]

    output.local(1, "John leaves.", [])

    calls = [
        call(
            "\r  John leaves.                                                              \n"
        ),
        call("\r\n> "),
    ]

    mock_client.send_message.assert_has_calls(calls)


def test_local_no_logged_in_clients(mock_client: Client):
    telnet = Mock()
    output = Output(telnet)

    telnet.get_connected_clients.return_value = [mock_client]

    output.local(1, "John leaves.", [])

    mock_client.send_message.assert_not_called()


def test_local_no_client_in_room(mock_client: Client):
    telnet = Mock()
    output = Output(telnet)

    mock_client.login_state = ClientLoginState.LOGGED_IN
    mock_client.player = Mock(current_room_id=2)

    telnet.get_connected_clients.return_value = [mock_client]

    output.local(1, "John leaves.", [])

    mock_client.send_message.assert_not_called()


def test_local_client_ignored(mock_client: Client):
    telnet = Mock()
    output = Output(telnet)

    mock_client.login_state = ClientLoginState.LOGGED_IN
    mock_client.player = Mock(current_room_id=1)

    telnet.get_connected_clients.return_value = [mock_client]

    output.local(1, "John leaves.", [mock_client])

    mock_client.send_message.assert_not_called()
