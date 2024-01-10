from pytest import fixture

from cibo.events import ConnectEvent, DisconnectEvent, InputEvent, SpawnEvent
from cibo.models import ClientLoginState
from cibo.models.server_config import ServerConfig
from tests.conftest import (
    BaseFactory,
    ClientFactory,
    CommandProcessorFactory,
    DatabaseFactory,
    MessageFactory,
    WorldFactory,
)


class ConnectEventFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_connect_event(self):
        self.connect = ConnectEvent(self.server_config)
        yield


class DisconnectEventFactory(BaseFactory, ClientFactory, MessageFactory):
    @fixture(autouse=True)
    def fixture_disconnect_event(self):
        self.client.login_state = ClientLoginState.LOGGED_IN
        self.disconnect = DisconnectEvent(self.server_config)
        yield


class InputEventFactory(CommandProcessorFactory, ClientFactory, MessageFactory):
    @fixture(autouse=True)
    def fixture_input_event(self):
        self.input = InputEvent(self.server_config, self.command_processor)
        yield


class SpawnEventFactory(BaseFactory, WorldFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_spawn_event(self):
        self.server_config = ServerConfig(self.telnet, self.world, self.comms)
        self.spawn = SpawnEvent(self.server_config)
        yield
