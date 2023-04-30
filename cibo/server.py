import threading

from cibo.telnet import TelnetServer

server = TelnetServer(port=51234)


clients = []

while True:
    # Make the server parse all the new events
    server_thread = threading.Thread(target=server.update(), args=[])
    server_thread.start()

    # For each newly connected client
    for new_client in server.get_new_clients():
        # Add them to the client list
        clients.append(new_client)
        # Send a welcome message
        server.send_message(new_client, f"Welcome, you are client {new_client}.")

    # For each client that has recently disconnected
    for disconnected_client in server.get_disconnected_clients():
        if disconnected_client not in clients:
            continue

        # Remove him from the clients list
        clients.remove(disconnected_client)

        # Send every client a message saying "Client X disconnected"
        for client in clients:
            server.send_message(client, f"Client {disconnected_client} disconnected.")

    # For each message a client has sent
    for sender_client, message in server.get_messages():
        if sender_client not in clients:
            continue

        # Send every client a message reading:
        # "I received "[MESSAGE]" from client [ID OF THE SENDER CLIENT]"
        for client in clients:
            server.send_message(
                client, f'I received "{message}" from client {sender_client}'
            )
