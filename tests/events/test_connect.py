from tests.conftest import ClientFactory, ConnectEventFactory


class TestConnectEvent(ClientFactory, ConnectEventFactory):
    def test_process(self):
        self.telnet.get_new_clients.return_value = [self.client]

        self.connect.process()

        self.output.private.assert_called_once()
