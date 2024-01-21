from cibo.models.event import EventPayload
from tests.events.conftest import ClientFactory, ConnectEventFactory


class TestConnectEvent(ClientFactory, ConnectEventFactory):
    def test_event_connect_process(self):
        self.signal.send(self, payload=EventPayload(self.client))

        self.comms.send_to_client.assert_called_once()

    def test_event_connect_process_no_payload(self):
        self.signal.send(self, payload=None)

        self.comms.send_to_client.assert_not_called()
