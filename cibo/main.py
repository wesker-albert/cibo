"""
This code is intended as temporary, while the meat and potatoes of the
server are being developed. TODO: instead use a daemonization approach where
the server is started and stopped from the commandline, and not while a loop is
running
"""

from time import sleep

from cibo.server import Server

if __name__ == "__main__":
    server = Server()

    print(
        "Accepted commands:\n\n"
        "create_db    create the necessary db and tables\n"
        "start        start the server\n"
        "stop         stop the server\n"
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
