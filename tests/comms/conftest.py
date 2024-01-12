from pytest import fixture

from cibo.comms._interface_ import CommsInterface
from cibo.comms.private import Private as CommsPrivate
from cibo.comms.region import Region as CommsRegion
from cibo.comms.room import Room as CommsRoom
from cibo.comms.sector import Sector as CommsSector
from cibo.comms.server import Server as CommsServer
from tests.conftest import BaseFactory, ClientFactory, EntityInterfaceFactory


class CommsFactory(BaseFactory, ClientFactory, EntityInterfaceFactory):
    @fixture(autouse=True)
    def fixture_comms(self, _fixture_mock_clients):
        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]
        self.comms = CommsInterface(self.telnet, self.entities)
        self.private = CommsPrivate(self.telnet, self.entities)
        self.room = CommsRoom(self.telnet, self.entities)
        self.sector = CommsSector(self.telnet, self.entities)
        self.region = CommsRegion(self.telnet, self.entities)
        self.server = CommsServer(self.telnet, self.entities)
        yield
