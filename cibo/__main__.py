""" This code is intended as temporary, while the meat and potatoes of the
server are being developed. TODO: instead use a daemonization approach where
the server is started and stopped from the commandline, and not while a loop is
running.
"""

from os import getenv
from time import sleep

from cibo.comms._interface_ import CommsInterface
from cibo.entities._interface_ import EntityInterface
from cibo.server import Server
from cibo.server_config import ServerConfig
from cibo.telnet import TelnetServer

if __name__ == "__main__":
    telnet = TelnetServer(port=int(getenv("SERVER_PORT", "51234")))
    entity_interface = EntityInterface()
    comms_interface = CommsInterface(telnet, entity_interface)

    server_config = ServerConfig(telnet, entity_interface, comms_interface)
    server = Server(server_config)

    print(
        "Accepted commands:\n\n"
        "create_db    create the necessary db and tables\n"
        "start        start the server\n"
        "stop         stop the server (currently broken, can't be started again)\n"
        "exit         stop the server if running, and exit this program\n"
    )

    while True:
        user_input = input("> ").lower()

        match user_input:
            case "create_db":
                server.create_db()

            case "start":
                if not server.is_running:
                    server.start()
                    print("Started server.")

                    continue

                if server.is_running:
                    print("Server is already running.")

            case "stop":
                if server.is_running:
                    server.stop()
                    print("Stopped server.")

                    continue

                if not server.is_running:
                    print("Server is not running.")

            case "exit":
                if server.is_running:
                    server.stop()
                    print("Stopped server.")

                print("Goodbye!")

                break

        sleep(1)
