from tests.conftest import ClientFactory, ConnectEventFactory


class TestConnectEvent(ClientFactory, ConnectEventFactory):
    def test_event_connect_process(self):
        self.telnet.get_new_clients.return_value = [self.client]

        self.connect.process()

        self.output.send_to_client.assert_called_once()
