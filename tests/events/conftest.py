from blinker import signal
from pytest import fixture

from cibo.events.connect import ConnectEvent
from cibo.events.disconnect import DisconnectEvent
from cibo.events.input import InputEvent
from cibo.events.spawn import SpawnEvent
from cibo.models.client import ClientLoginState
from cibo.server_config import ServerConfig
from tests.conftest import (
    BaseFactory,
    ClientFactory,
    CommandProcessorFactory,
    DatabaseFactory,
    EntityInterfaceFactory,
    MessageFactory,
)


class ConnectEventFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_connect_event(self):
        self.connect = ConnectEvent(self.server_config, "event-connect")
        self.signal = signal("event-connect")
        yield


class DisconnectEventFactory(BaseFactory, ClientFactory, MessageFactory):
    @fixture(autouse=True)
    def fixture_disconnect_event(self):
        self.client.login_state = ClientLoginState.LOGGED_IN
        self.disconnect = DisconnectEvent(self.server_config, "event-disconnect")
        self.signal = signal("event-disconnect")
        yield


class InputEventFactory(CommandProcessorFactory, ClientFactory, MessageFactory):
    @fixture(autouse=True)
    def fixture_input_event(self):
        self.input = InputEvent(
            self.server_config, "event-input", self.command_processor
        )
        self.signal = signal("event-input")
        yield


class SpawnEventFactory(BaseFactory, EntityInterfaceFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_spawn_event(self):
        self.server_config = ServerConfig(self.telnet, self.entities, self.comms)
        self.spawn = SpawnEvent(self.server_config, "event-spawn")
        self.signal = signal("event-spawn")
        yield
