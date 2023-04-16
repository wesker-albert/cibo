"""Basic Telnet server module.

Contains one class, TelnetServer, which can be instantiated to start a
server running then used to send and receive messages from clients.

It is a generalization made by Oliver L. Sanz from Mark Frimston's
mud-py server.

Further modified as needed, to accomodate the cibo project.
"""


import select
import socket
import time
from uuid import uuid4


class TelnetServer:
    """A basic Telnet server.
    Once created, the server will listen for clients connecting using
    Telnet. Messages can then be sent to and from multiple connected
    clients.
    The 'update' method should be called in a loop to keep the server
    running.
    """

    # An inner class which is instantiated for each connected client to store
    # info about them

    class _Client:  # pylint: disable=too-few-public-methods
        """Holds information about a connected client"""

        # the socket object used to communicate with this client
        socket = None
        # the ip address of this client
        address = ""
        # holds data send from the client until a full message is received
        buffer = ""
        # the last time we checked if the client was still connected
        lastcheck = 0

        def __init__(self, socket_, address, buffer, lastcheck):
            self.socket = socket_
            self.address = address
            self.buffer = buffer
            self.lastcheck = lastcheck

    # Used to store different types of occurences
    _EVENT_NEW_client = 1
    _EVENT_client_LEFT = 2
    _EVENT_MESSAGE = 3

    # Different states we can be in while reading data from client
    # See _process_sent_data function
    _READ_STATE_NORMAL = 1
    _READ_STATE_MESSAGE = 2
    _READ_STATE_SUBNEG = 3

    # Command codes used by Telnet protocol
    # See _process_sent_data function
    _TN_INTERPRET_AS_MESSAGE = 255
    _TN_ARE_YOU_THERE = 246
    _TN_WILL = 251
    _TN_WONT = 252
    _TN_DO = 253
    _TN_DONT = 254
    _TN_SUBNEGOTIATION_START = 250
    _TN_SUBNEGOTIATION_END = 240

    # socket used to listen for new clients
    _listen_socket = None
    # holds info on clients. Maps client id to _Client object
    _clients = {}
    # list of occurences waiting to be handled by the code
    _events = []
    # list of newly-added occurences
    _new_events = []

    # pylint: disable=line-too-long
    def __init__(self, encoding="utf-8", error_policy="replace", port=1234):
        """Constructs the TelnetServer object and starts listening for
        new clients.

        Args:
            encoding (str, optional): Enconding of the data to be processed. Valid values are specified here: https://docs.python.org/3/howto/unicode.html. Defaults to "utf-8".
            error_policy (str, optional): What to do when a character cannot be decoded. Valid values are specified here: https://docs.python.org/3/howto/unicode.html. Defaults to 'replace'.
            port (int, optional): port for the server.

        Returns:
            [type]: [description]
        """
        self.error_policy = error_policy
        self.encoding = encoding
        self._clients = {}
        self._events = []
        self._new_events = []

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
        self._listen_socket.bind(("0.0.0.0", port))

        # set to non-blocking mode. This means that when we call 'accept', it
        # will return immediately without waiting for a connection
        self._listen_socket.setblocking(False)

        # start listening for connections on the socket
        self._listen_socket.listen(1)

    def update(self):
        """Checks for new clients, disconnected clients, and new
        messages sent from clients. This method must be called before
        up-to-date info can be obtained from the 'get_new_clients',
        'get_disconnected_clients' and 'get_messages' methods.
        It should be called in a loop to keep the server running.
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

    def get_new_clients(self):
        """Returns a list containing info on any new clients that have
        entered the server since the last call to 'update'. Each item in
        the list is a client id number.
        """
        retval = []
        # go through all the events in the main list
        for event in self._events:
            # if the event is a new client occurence, add the info to the list
            if event[0] == self._EVENT_NEW_client:
                retval.append(event[1])
        # return the info list
        return retval

    def get_disconnected_clients(self):
        """Returns a list containing info on any clients that have left
        the server since the last call to 'update'. Each item in the list
        is a client id number.
        """
        retval = []
        # go through all the events in the main list
        for event in self._events:
            # if the event is a client disconnect occurence, add the info to
            # the list
            if event[0] == self._EVENT_client_LEFT:
                retval.append(event[1])
        # return the info list
        return retval

    def get_messages(self):
        """Returns a list containing any messages sent from clients
        since the last call to 'update'. Each item in the list is a
        2-tuple containing the id number of the sending client, and
        a string containing the message sent by the user.
        """
        retval = []
        # go through all the events in the main list
        for event in self._events:
            # if the event is a message occurence, add the info to the list
            if event[0] == self._EVENT_MESSAGE:
                retval.append((event[1], event[2]))
        # return the info list
        return retval

    def send_message(self, to_, message):
        """Sends the text in the 'message' parameter to the client with
        the id number given in the 'to' parameter. The text will be
        printed out in the client's terminal.
        """
        # we make sure to put a newline on the end so the client receives the
        # message on its own line
        self._attempt_send(to_, message + "\n\r")

    def shutdown(self):
        """Closes down the server, disconnecting all clients and
        closing the listen socket.
        """
        # for each client
        for client in self._clients.values():
            # close the socket, disconnecting the client
            client.socket.shutdown(socket.SHUT_RDWR)
            client.socket.close()
        # stop listening for new clients
        self._listen_socket.close()

    def _attempt_send(self, clid, data):
        try:
            # look up the client in the client map and use 'sendall' to send
            # the message string on the socket. 'sendall' ensures that all of
            # the data is sent in one go
            self._clients[clid].socket.sendall(bytearray(data, self.encoding))
        # KeyError will be raised if there is no client with the given id in
        # the map
        except KeyError:
            pass
        # If there is a connection problem with the client (e.g. they have
        # disconnected) a socket error will be raised
        except socket.error:
            self._handle_disconnect(clid)

    def _check_for_new_connections(self):
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
        joined_socket, addr = self._listen_socket.accept()

        # set non-blocking mode on the new socket. This means that 'send' and
        # 'recv' will return immediately without waiting
        joined_socket.setblocking(False)

        # generate a uuid that serves as the client id
        client_id = uuid4()

        # construct a new _Client object to hold info about the newly connected
        # client. Use 'client_id' as the new client's id number
        self._clients[client_id] = TelnetServer._Client(
            joined_socket, addr[0], "", time.time()
        )

        # add a new client occurence to the new events list with the client's
        # id number
        self._new_events.append((self._EVENT_NEW_client, client_id))

    def _check_for_disconnected(self):
        # go through all the clients
        for id_, client in list(self._clients.items()):
            # if we last checked the client less than 5 seconds ago, skip this
            # client and move on to the next one
            if time.time() - client.lastcheck < 5.0:
                continue

            # send the client an invisible character. It doesn't actually
            # matter what we send, we're really just checking that data can
            # still be written to the socket. If it can't, an error will be
            # raised and we'll know that the client has disconnected.
            self._attempt_send(id_, "\x00")

            # update the last check time
            client.lastcheck = time.time()

    def _check_for_messages(self):
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
                    self._new_events.append((self._EVENT_MESSAGE, id_, message))

            # if there is a problem reading from the socket (e.g. the client
            # has disconnected) a socket error will be raised
            except socket.error:
                self._handle_disconnect(id_)

    def _handle_disconnect(self, clid):
        # remove the client from the clients map
        del self._clients[clid]

        # add a 'client left' occurence to the new events list, with the
        # client's id number
        self._new_events.append((self._EVENT_client_LEFT, clid))

    def _process_sent_data(self, client, data):
        # the Telnet protocol allows special message codes to be inserted into
        # messages. For our very simple server we don't need to response to
        # any of these codes, but we must at least detect and skip over them
        # so that we don't interpret them as text data.
        # More info on the Telnet protocol can be found here:
        # http://pcmicro.com/netfoss/telnet.html

        # start with no message and in the normal state
        message = None
        state = self._READ_STATE_NORMAL

        # go through the data a character at a time
        for char in data:
            # handle the character differently depending on the state we're in:

            # normal state
            if state == self._READ_STATE_NORMAL:
                # if we received the special 'interpret as message' code,
                # switch to 'message' state so that we handle the next
                # character as a message code and not as regular text data
                if ord(char) == self._TN_INTERPRET_AS_MESSAGE:
                    state = self._READ_STATE_MESSAGE

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
            elif state == self._READ_STATE_MESSAGE:
                # the special 'start of subnegotiation' message code indicates
                # that the following characters are a list of options until
                # we're told otherwise. We switch into 'subnegotiation' state
                # to handle this
                if ord(char) == self._TN_SUBNEGOTIATION_START:
                    state = self._READ_STATE_SUBNEG

                # if the message code is one of the 'will', 'wont', 'do' or
                # 'dont' messages, the following character will be an option
                # code so we must remain in the 'message' state
                elif ord(char) in (
                    self._TN_WILL,
                    self._TN_WONT,
                    self._TN_DO,
                    self._TN_DONT,
                ):
                    state = self._READ_STATE_MESSAGE

                # for all other message codes, there is no accompanying data so
                # we can return to 'normal' state.
                else:
                    state = self._READ_STATE_NORMAL

            # subnegotiation state
            elif state == self._READ_STATE_SUBNEG:
                # if we reach an 'end of subnegotiation' message, this ends the
                # list of options and we can return to 'normal' state.
                # Otherwise we must remain in this state
                if ord(char) == self._TN_SUBNEGOTIATION_END:
                    state = self._READ_STATE_NORMAL

        # return the contents of 'message' which is either a string or None
        message = client.buffer
        client.buffer = ""
        return message
