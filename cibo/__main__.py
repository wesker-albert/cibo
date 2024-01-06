""" This code is intended as temporary, while the meat and potatoes of the
server are being developed. TODO: instead use a daemonization approach where
the server is started and stopped from the commandline, and not while a loop is
running.
"""

from os import getenv
from time import sleep

from cibo.config import ServerConfig
from cibo.resources.world import World
from cibo.server import Server
from cibo.telnet import TelnetServer

if __name__ == "__main__":
    telnet = TelnetServer(port=int(getenv("SERVER_PORT", "51234")))
    world = World()

    server_config = ServerConfig(telnet, world)
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

        if user_input == "create_db":
            server.create_db()

        if user_input == "start":
            if not server.is_running:
                server.start()

                print("Started server.")

                continue

            if server.is_running:
                print("Server is already running.")

        if user_input == "stop":
            if server.is_running:
                server.stop()
                print("Stopped server.")

                continue

            if not server.is_running:
                print("Server is not running.")

        if user_input == "exit":
            if server.is_running:
                server.stop()
                print("Stopped server.")

            print("Goodbye!")
            break

        sleep(1)
