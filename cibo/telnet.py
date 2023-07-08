"""
Basic Telnet server module.

Contains one class, TelnetServer, which can be instantiated to start a server running
then used to send and receive messages from clients.

It is a generalization made by Oliver L. Sanz from Mark Frimston's mud-py server.

Further modified as needed, to accomodate the cibo project.
"""

import select
import socket
import time
from enum import Enum
from typing import Dict, List, Tuple
from uuid import UUID, uuid4

from cibo.models.client import Client, ClientLoginState


class TelnetServer:
    """
    A basic Telnet server.

    Once created, the server will listen for clients connecting using Telnet. Messages
    can then be sent to and from multiple connected clients.

    The 'update' method should be called in a loop to keep the server running.
    """

    class Event(int, Enum):
        """Different types of occurances."""

        NEW_CLIENT = 1
        CLIENT_LEFT = 2
        MESSAGE = 3

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
        self, encoding: str = "utf-8", error_policy: str = "replace", port: int = 1234
    ) -> None:
        """
        Constructs the TelnetServer object and starts listening for new clients.

        Valid arg values specified here: https://docs.python.org/3/howto/unicode.html

        Args:
            encoding (str, optional): Encoding of the data to be processed
            error_policy (str, optional): What to do when a character cannot be decoded
            port (int, optional): port for the server
        """
        self.encoding = encoding
        self.error_policy = error_policy
        self.port = port

        self._listen_socket = None
        self._clients: Dict[UUID, Client] = {}
        self._events = []
        self._new_events = []

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
        self._listen_socket.bind(("0.0.0.0", self.port))

        # set to non-blocking mode. This means that when we call 'accept', it
        # will return immediately without waiting for a connection
        self._listen_socket.setblocking(False)

        # start listening for connections on the socket
        self._listen_socket.listen(1)

    def update(self) -> None:
        """
        Checks for new clients, disconnected clients, and new messages sent from
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
        self._events = list(self._new_events)
        self._new_events = []

    def get_new_clients(self) -> List[UUID]:
        """
        Returns a list containing info on any new clients that have connected to the
        server since the last call to 'update'.

        Returns:
            List[UUID]: Each item is a client ID number
        """

        client_ids = []

        # go through all the events in the main list
        for event in self._events:
            # if the event is a new client occurence, add the info to the list
            if event[0] == self.Event.NEW_CLIENT:
                client_ids.append(event[1])

        # return the info list
        return client_ids

    def get_disconnected_clients(self) -> List[UUID]:
        """
        Returns a list containing info on any clients that have left the server since
        the last call to 'update'.

        Returns:
            List[UUID]: Each item is a client ID number
        """

        client_ids = []

        # go through all the events in the main list
        for event in self._events:
            # if the event is a client disconnect occurence, add the info to
            # the list
            if event[0] == self.Event.CLIENT_LEFT:
                client_ids.append(event[1])

        # return the info list
        return client_ids

    def get_input(self) -> List[Tuple[UUID, str]]:
        """
        Returns a list containing any messages sent from clients since the last call
        to 'update'.

        Returns:
            List[Tuple[UUID, str]]: The client ID, and the incoming message they sent
        """

        client_messages = []

        # go through all the events in the main list
        for event in self._events:
            # if the event is a message occurence, add the info to the list
            if event[0] == self.Event.MESSAGE:
                client_messages.append((event[1], event[2]))

        # return the info list
        return client_messages

    def send_message(self, client_id: UUID, message: str) -> None:
        """
        Sends the text in the 'message' parameter to the client with the id number
        given in the 'to' parameter. The text will be printed out in the client's
        terminal.

        Args:
            client_id (UUID): The ID of the client to send the message to
            message (str): The body text of the message
        """

        # we make sure to put a newline on the end so the client receives the
        # message on its own line
        self._attempt_send(client_id, f"{message}\n\r")

    def shutdown(self) -> None:
        """
        Closes down the server, disconnecting all clients and closing the listen socket.
        """

        # for each client
        for client in self._clients.values():
            # close the socket, disconnecting the client
            client.socket.shutdown(socket.SHUT_RDWR)
            client.socket.close()

        # stop listening for new clients
        if self._listen_socket:
            self._listen_socket.close()

    def _attempt_send(self, client_id: UUID, data: str) -> None:
        try:
            # look up the client in the client map and use 'sendall' to send
            # the message string on the socket. 'sendall' ensures that all of
            # the data is sent in one go
            self._clients[client_id].socket.sendall(bytearray(data, self.encoding))

        # KeyError will be raised if there is no client with the given id in
        # the map
        except KeyError:
            pass

        # If there is a connection problem with the client (e.g. they have
        # disconnected) a socket error will be raised
        except socket.error:
            self._handle_disconnect(client_id)

    def _check_for_new_connections(self) -> None:
        # 'select' is used to check whether there is data waiting to be read
        # from the socket. We pass in 3 lists of sockets, the first being those
        # to check for readability. It returns 3 lists, the first being
        # the sockets that are readable. The last parameter is how long to wait
        # - we pass in 0 so that it returns immediately without waiting
        rlist, _wlist, _xlist = select.select([self._listen_socket], [], [], 0)

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

            # generate a uuid that serves as the client id
            client_id = uuid4()

            # construct a new Client object to hold info about the newly connected
            # client. Use 'client_id' as the new client's id number
            self._clients[client_id] = Client(
                id_=client_id,
                socket=joined_socket,
                address=addr[0],
                buffer="",
                last_check=time.time(),
                login_state=ClientLoginState.PRE_LOGIN,
                player=None,
            )

            # add a new client occurence to the new events list with the client's
            # id number
            self._new_events.append((self.Event.NEW_CLIENT, client_id))

    def _check_for_disconnected(self) -> None:
        # go through all the clients
        for id_, client in list(self._clients.items()):
            # if we last checked the client less than 5 seconds ago, skip this
            # client and move on to the next one
            if time.time() - client.last_check < 5.0:
                continue

            # send the client an invisible character. It doesn't actually
            # matter what we send, we're really just checking that data can
            # still be written to the socket. If it can't, an error will be
            # raised and we'll know that the client has disconnected.
            self._attempt_send(id_, "\x00")

            # update the last check time
            client.last_check = time.time()

    def _check_for_messages(self) -> None:
        # go through all the clients
        for id_, client in list(self._clients.items()):
            # we use 'select' to test whether there is data waiting to be read
            # from the client socket. The function takes 3 lists of sockets,
            # the first being those to test for readability. It returns 3 list
            # of sockets, the first being those that are actually readable.
            rlist, _wlist, _xlist = select.select([client.socket], [], [], 0)

            # if the client socket wasn't in the readable list, there is no
            # new data from the client - we can skip it and move on to the next
            # one
            if client.socket not in rlist:
                continue

            try:
                # read data from the socket, using a max length of 4096
                data = client.socket.recv(4096).decode(self.encoding, self.error_policy)

                # process the data, stripping out any special Telnet messages
                message = self._process_sent_data(client, data)

                # if there was a message in the data
                if message:
                    # remove any spaces, tabs etc from the start and end of
                    # the message
                    message = message.strip()

                    # add a message occurence to the new events list with the
                    # client's id number, and the message
                    self._new_events.append((self.Event.MESSAGE, id_, message))

            # if there is a problem reading from the socket (e.g. the client
            # has disconnected) a socket error will be raised
            except socket.error:
                self._handle_disconnect(id_)

    def _handle_disconnect(self, client_id: UUID) -> None:
        # remove the client from the clients map
        del self._clients[client_id]

        # add a 'client left' occurence to the new events list, with the
        # client's id number
        self._new_events.append((self.Event.CLIENT_LEFT, client_id))

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
