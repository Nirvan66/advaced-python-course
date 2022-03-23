import socket

from click import command

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
    socket_client.connect(("127.0.0.1", 5075))

    welcome_message = socket_client.recv(2048)

    print(welcome_message.decode())

    while True:
        command = input("> ")
        if command=="exit":
            socket_client.close()
            break
        else:
            socket_client.sendall(command.encode())
            print(socket_client.recv(2048).decode())


