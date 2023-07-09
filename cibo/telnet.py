"""Basic Telnet server module.

Based on a generalization made by Oliver L. Sanz from Mark Frimston's mud-py server.
https://github.com/OliverLSanz/python-telnetserver/blob/master/telnetserver

Further modified as needed, to accomodate the cibo project.
"""

import socket
import time
from dataclasses import dataclass
from enum import Enum
from select import select
from typing import Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from cibo.models.client import Client, ClientLoginState


class TelnetEventType(int, Enum):
    """Different types of incoming events from clients."""

    NEW_CLIENT = 1
    CLIENT_LEFT = 2
    MESSAGE = 3


@dataclass
class TelnetEvent:
    """An incoming telnet event, including important data."""

    type_: TelnetEventType
    client_id: UUID
    client: Client
    message: Optional[str] = None


class TelnetServer:
    """A basic Telnet server.

    Once created, the server will listen for clients connecting using Telnet. Messages
    can then be sent to and from multiple connected clients.

    The 'update' method should be called in a loop to keep the server running.
    """

    class ReadState(int, Enum):
        """Different states we can be in while reading data from client."""

        NORMAL = 1
        MESSAGE = 2
        SUBNEG = 3

    class CommandCode(int, Enum):
        """Command codes used by Telnet protocol."""

        INTERPRET_AS_MESSAGE = 255
        ARE_YOU_THERE = 246
        WILL = 251
        WONT = 252
        DO = 253
        DONT = 254
        SUBNEGOTIATION_START = 250
        SUBNEGOTIATION_END = 240

    def __init__(
        self, port: int, encoding: str = "utf-8", error_policy: str = "replace"
    ) -> None:
        """Constructs the TelnetServer object and starts listening for new clients.

        Valid arg values specified here: https://docs.python.org/3/howto/unicode.html

        Args:
            port (int): Port for the server
            encoding (str, optional): Encoding of the data to be processed
            error_policy (str, optional): What to do when a character cannot be decoded
        """
        self._encoding = encoding
        self._error_policy = error_policy
        self._port = port

        self._listen_socket: Optional[socket.socket] = None
        self._events: List[TelnetEvent] = []
        self._new_events: List[TelnetEvent] = []

        self._clients: Dict[UUID, Client] = {}

    def listen(self) -> None:
        """Configure the socket and begin listening."""

        # create a new tcp socket which will be used to listen for new clients
        self._listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set a special option on the socket which allows the port to be
        # immediately without having to wait
        self._listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to an ip address and port. Port 23 is the standard
        # telnet port which telnet clients will use, however on some platforms
        # this requires root permissions, so we use a higher arbitrary port
        # number instead: 1234. Address 0.0.0.0 means that we will bind to all
        # of the available network interfaces
        self._listen_socket.bind(("0.0.0.0", self._port))

        # set to non-blocking mode. This means that when we call 'accept', it
        # will return immediately without waiting for a connection
        self._listen_socket.setblocking(False)

        # start listening for connections on the socket
        self._listen_socket.listen(1)

    def update(self) -> None:
        """Checks for new clients, disconnected clients, and new messages sent from
        clients. This method must be called before up-to-date info can be obtained
        from the 'get_new_clients', 'get_disconnected_clients' and 'get_messages'
        methods. It should be called in a loop to keep the server running.
        """

        # check for new stuff
        self._check_for_new_connections()
        self._check_for_disconnected()
        self._check_for_messages()

        # move the new events into the main events list so that they can be
        # obtained with 'get_new_clients', 'get_disconnected_clients' and
        # 'get_messages'. The previous events are discarded
        self._events = self._new_events
        self._new_events = []

    def get_new_clients(self) -> List[Client]:
        """Returns a list containing any new clients that have connected to the server
        since the last call to 'update'.

        Returns:
            List[Client]: All newly connected clients
        """

        clients = [
            event.client
            for event in self._events
            if event.type_ is TelnetEventType.NEW_CLIENT
        ]

        return clients

    def get_connected_clients(self) -> List[Client]:
        """Returns a list of all currently connected clients, as of last call to
        'update'.

        Returns:
            List[Client]: All cuurently connected clients
        """

        return list(self._clients.values())

    def get_disconnected_clients(self) -> List[Client]:
        """Returns a list containing the clients that have left the server since the
        last call to 'update'.

        Returns:
            List[Client]: Clients who have disconnected
        """

        clients = [
            event.client
            for event in self._events
            if event.type_ is TelnetEventType.CLIENT_LEFT
        ]

        return clients

    def get_client_input(self) -> List[Tuple[Client, Optional[str]]]:
        """Returns a list containing any messages sent from clients since the last call
        to 'update'.

        Returns:
            List[Tuple[Client, Optional[str]]]: The client and the incoming message
                they sent
        """

        client_messages = [
            (event.client, event.message)
            for event in self._events
            if event.type_ is TelnetEventType.MESSAGE
        ]

        return client_messages

    def send_message(self, client: Client, message: str) -> None:
        """Sends the message text to the given client. The text will be printed out in
        the client's terminal.

        Args:
            client (Client): The client to send the message to
            message (str): The body text of the message
        """

        # we make sure to put a newline on the end so the client receives the
        # message on its own line
        self._attempt_send(client, f"{message}\n\r")

    def shutdown(self) -> None:
        """Closes down the server, disconnecting all clients and closing the listen
        socket.
        """

        # for each client
        for client in self._clients.values():
            # close the socket, disconnecting the client
            client.socket.shutdown(socket.SHUT_RDWR)
            client.socket.close()

        # stop listening for new clients
        if self._listen_socket:
            self._listen_socket.close()

    def _attempt_send(self, client: Client, data: str) -> None:
        try:
            # use 'sendall' to send the message string on the socket. 'sendall'
            # ensures that all of the data is sent in one go
            client.socket.sendall(bytearray(data, self._encoding))

        # If there is a connection problem with the client (e.g. they have
        # disconnected) a socket error will be raised
        except socket.error:
            self._handle_disconnect(client)

    def _check_for_new_connections(self) -> None:
        # 'select' is used to check whether there is data waiting to be read
        # from the socket. We pass in 3 lists of sockets, the first being those
        # to check for readability. It returns 3 lists, the first being
        # the sockets that are readable. The last parameter is how long to wait
        # - we pass in 0 so that it returns immediately without waiting
        rlist, _wlist, _xlist = select([self._listen_socket], [], [], 0)

        # if the socket wasn't in the readable list, there's no data available,
        # meaning no clients waiting to connect, and so we can exit the method
        # here
        if self._listen_socket not in rlist:
            return

        # 'accept' returns a new socket and address info which can be used to
        # communicate with the new client
        if self._listen_socket:
            joined_socket, addr = self._listen_socket.accept()

            # set non-blocking mode on the new socket. This means that 'send' and
            # 'recv' will return immediately without waiting
            joined_socket.setblocking(False)

            # construct a new Client object to hold info about the newly connected
            # client. Use a UUID as the new client's id number
            new_client = Client(
                id_=uuid4(),
                socket=joined_socket,
                address=addr[0],
                buffer="",
                last_check=time.time(),
                login_state=ClientLoginState.PRE_LOGIN,
                player=None,
            )

            self._clients[new_client.id_] = new_client

            # add a new client occurence to the new events list with the client's
            # id number
            self._new_events.append(
                TelnetEvent(TelnetEventType.NEW_CLIENT, new_client.id_, new_client)
            )

    def _check_for_disconnected(self) -> None:
        # go through all the clients
        for client in list(self._clients.values()):
            # if we last checked the client less than 5 seconds ago, skip this
            # client and move on to the next one
            if time.time() - client.last_check < 5.0:
                continue

            # send the client an invisible character. It doesn't actually
            # matter what we send, we're really just checking that data can
            # still be written to the socket. If it can't, an error will be
            # raised and we'll know that the client has disconnected.
            self._attempt_send(client, "\x00")

            # update the last check time
            client.last_check = time.time()

    def _check_for_messages(self) -> None:
        # go through all the clients
        for client in list(self._clients.values()):
            # we use 'select' to test whether there is data waiting to be read
            # from the client socket. The function takes 3 lists of sockets,
            # the first being those to test for readability. It returns 3 list
            # of sockets, the first being those that are actually readable.
            rlist, _wlist, _xlist = select([client.socket], [], [], 0)

            # if the client socket wasn't in the readable list, there is no
            # new data from the client - we can skip it and move on to the next
            # one
            if client.socket not in rlist:
                continue

            try:
                # read data from the socket, using a max length of 4096
                data = client.socket.recv(4096).decode(
                    self._encoding, self._error_policy
                )

                # process the data, stripping out any special Telnet messages
                message = self._process_sent_data(client, data)

                # if there was a message in the data
                if message:
                    # remove any spaces, tabs etc from the start and end of
                    # the message
                    message = message.strip()

                    # add a message occurence to the new events list with the
                    # client's id number, and the message
                    self._new_events.append(
                        TelnetEvent(
                            TelnetEventType.MESSAGE, client.id_, client, message
                        )
                    )

            # if there is a problem reading from the socket (e.g. the client
            # has disconnected) a socket error will be raised
            except socket.error:
                self._handle_disconnect(client)

    def _handle_disconnect(self, client: Client) -> None:
        # remove the client from the clients map
        del self._clients[client.id_]

        # add a 'client left' occurence to the new events list, with the
        # client's id number
        self._new_events.append(
            TelnetEvent(TelnetEventType.CLIENT_LEFT, client.id_, client)
        )

    def _process_sent_data(self, client: Client, data: str) -> str:
        # the Telnet protocol allows special message codes to be inserted into
        # messages. For our very simple server we don't need to response to
        # any of these codes, but we must at least detect and skip over them
        # so that we don't interpret them as text data.
        # More info on the Telnet protocol can be found here:
        # http://pcmicro.com/netfoss/telnet.html

        # start with no message and in the normal state
        message = None
        state = self.ReadState.NORMAL

        # go through the data a character at a time
        for char in data:
            # handle the character differently depending on the state we're in:

            # normal state
            if state == self.ReadState.NORMAL:
                # if we received the special 'interpret as message' code,
                # switch to 'message' state so that we handle the next
                # character as a message code and not as regular text data
                if ord(char) == self.CommandCode.INTERPRET_AS_MESSAGE:
                    state = self.ReadState.MESSAGE

                # some telnet clients send the characters as soon as the user
                # types them. So if we get a backspace character, this is where
                # the user has deleted a character and we should delete the
                # last character from the buffer.
                elif char == "\x08":
                    client.buffer = client.buffer[:-1]

                # otherwise it's just a regular character - add it to the
                # buffer where we're building up the received message
                else:
                    client.buffer += char

            # message state
            elif state == self.ReadState.MESSAGE:
                # the special 'start of subnegotiation' message code indicates
                # that the following characters are a list of options until
                # we're told otherwise. We switch into 'subnegotiation' state
                # to handle this
                if ord(char) == self.CommandCode.SUBNEGOTIATION_START:
                    state = self.ReadState.SUBNEG

                # if the message code is one of the 'will', 'wont', 'do' or
                # 'dont' messages, the following character will be an option
                # code so we must remain in the 'message' state
                elif ord(char) in (
                    self.CommandCode.WILL,
                    self.CommandCode.WONT,
                    self.CommandCode.DO,
                    self.CommandCode.DONT,
                ):
                    state = self.ReadState.MESSAGE

                # for all other message codes, there is no accompanying data so
                # we can return to 'normal' state.
                else:
                    state = self.ReadState.NORMAL

            # subnegotiation state
            elif state == self.ReadState.SUBNEG:
                # if we reach an 'end of subnegotiation' message, this ends the
                # list of options and we can return to 'normal' state.
                # Otherwise we must remain in this state
                if ord(char) == self.CommandCode.SUBNEGOTIATION_END:
                    state = self.ReadState.NORMAL

        # return the contents of 'message' which is either a string or None
        message = client.buffer
        client.buffer = ""
        return message
