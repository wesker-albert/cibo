from pytest import fixture

from cibo.actions import Connect, Disconnect, Error
from cibo.actions.commands import (
    Close,
    Drop,
    Exits,
    Finalize,
    Get,
    Inventory,
    Login,
    Logout,
    Look,
    Move,
    Open,
    Quit,
    Register,
    Say,
)
from cibo.actions.scheduled import EveryMinute, EverySecond
from cibo.models import ClientLoginState
from cibo.models.data import Player
from cibo.server_config import ServerConfig
from tests.conftest import (
    BaseFactory,
    ClientFactory,
    DatabaseFactory,
    MessageFactory,
    WorldFactory,
)


class ActionFactory(ClientFactory, WorldFactory, MessageFactory):
    def get_message_panel(self):
        return self.comms.send_to_client.call_args.args[0].message.body

    @fixture
    def _fixture_action(self, _fixture_world):
        self.server_config = ServerConfig(self.telnet, self.world, self.comms)
        self.client.login_state = ClientLoginState.LOGGED_IN
        yield


class ConnectActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_connect(self, _fixture_action):
        self.connect = Connect(self.server_config)
        yield


class DisconnectActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_disconnect(self, _fixture_action):
        self.disconnect = Disconnect(self.server_config)
        yield


class ErrorActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_error(self, _fixture_action):
        self.error = Error(self.server_config)
        yield


class CloseActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_close(self, _fixture_action):
        self.close = Close(self.server_config)
        yield


class OpenActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_open(self, _fixture_action):
        self.open = Open(self.server_config)
        yield


class MoveActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_move(self, _fixture_action):
        self.telnet.get_connected_clients.return_value = []
        self.move = Move(self.server_config)
        yield


class LookActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_look(self, _fixture_action):
        self.look = Look(self.server_config)
        yield


class ExitsActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_exits(self, _fixture_action):
        self.exits = Exits(self.server_config)
        yield


class SayActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_say(self, _fixture_action):
        self.say = Say(self.server_config)
        yield


class QuitActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_quit(self, _fixture_action):
        self.quit = Quit(self.server_config)
        yield


class LogoutActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_logout(self, _fixture_action):
        self.logout = Logout(self.server_config)
        yield


class RegisterActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_register(self, _fixture_action):
        self.client.login_state = ClientLoginState.PRE_LOGIN
        self.register = Register(self.server_config)
        yield


class FinalizeActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_finalize(self, _fixture_action):
        self.client.login_state = ClientLoginState.PRE_LOGIN
        self.client.registration = Player()
        self.finalize = Finalize(self.server_config)
        yield


class LoginActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_login(self, _fixture_action):
        self.client.login_state = ClientLoginState.PRE_LOGIN
        self.login = Login(self.server_config)
        yield


class InventoryActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_inventory(self, _fixture_action):
        self.inventory = Inventory(self.server_config)
        yield


class DropActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_drop(self, _fixture_action):
        self.drop = Drop(self.server_config)
        yield


class GetActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_get(self, _fixture_action):
        self.get = Get(self.server_config)
        yield


class EveryMinuteActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_every_minute(self, _fixture_action):
        self.every_minute = EveryMinute(self.server_config)
        yield


class EverySecondActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_every_second(self, _fixture_action):
        self.every_second = EverySecond(self.server_config)
        yield
