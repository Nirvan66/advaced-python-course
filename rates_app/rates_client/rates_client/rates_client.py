""" rate client module """
import sys
from contextlib import contextmanager
from collections.abc import Generator
import socket
from rates_shared.rates_shared import HOST, PORT


@contextmanager
def server_client_socket(host, port) -> Generator[socket.socket, None, None]:
    # implement socket client
    # - use "AF_INET" for IPv4
    # - use "SOCK_STREAM" for TCP
    # connect to localhost and port 5050 using the context manager
    # print the welcome message from the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
        socket_client.connect((host, port))

        welcome_message = socket_client.recv(2048)

        print(welcome_message.decode())

        yield socket_client

        socket_client.close()

def main() -> None:
    try:
        with server_client_socket(HOST, PORT) as socket_client:
            # display a command prompt, allow the user to enter text
            # send the user entered text to the server, then receive the response
            # and output the response to the console
            while True:
                command = input("> ")
                if command == "exit":
                    break
                else:
                    socket_client.sendall(command.encode())
                    print(socket_client.recv(2048).decode())
        pass

    except ConnectionResetError:
        print("Server connection was closed.")

    except ConnectionRefusedError:
        print("Server not found.")

    except KeyboardInterrupt:
        pass

    sys.exit(0)
