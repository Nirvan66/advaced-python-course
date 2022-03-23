""" rate server module """
from typing import Optional
from contextlib import contextmanager
from collections.abc import Generator
import sys
import socket

import multiprocessing as mp

HOST = "127.0.0.1"
PORT = 5075


@contextmanager
def server_client_connection(host, port) -> Generator[socket.socket, None, None]:
    # use "AF_INET" for IPv4
    # use "SOCK_STREAM" for TCP
    # when a client connects, send the following string:
    # "Connected to the Rate Server"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        socket_server.bind((host, port))
        socket_server.listen()
        print(f"server is listening on {host}:{port}")
        # blocking call waiting for client to connect
        conn, addr = socket_server.accept()
        print(f"Client at {addr[0]}:{addr[1]}, ",
              "connected to the Rate Server")

        conn.sendall(f"Welcome to {HOST}:{PORT}".encode())

        yield conn
        
        print("Client has left. Imma finna leave. Peace!!!")
        socket_server.close()


def rate_server(host, port) -> None:
    """rate server"""
    # implement socket server
    # the host and port should be received as parameters into this function
    with server_client_connection(host, port) as client_connection:
        # wire up an echo server which receives a string and echos back to
        while True:
            message = client_connection.recv(2048).decode()
            if not message:
                break
            print(f"recv: {message}")
            client_connection.sendall(message.encode())


def command_start_server(server_process: Optional[mp.Process]) -> mp.Process:
    """ command start server """

    if server_process and server_process.is_alive():
        print("server is already running")
    else:
        # step 1 - create a new process object
        server_process = mp.Process(target=rate_server, args=(HOST, PORT,))
        # step 2 - start the new process object
        server_process.start()
        print("server started")

    return server_process


def command_stop_server(
        server_process: Optional[mp.Process]) -> Optional[mp.Process]:
    """ command stop server """

    if not server_process or not server_process.is_alive():
        print("server is not running")
    else:
        server_process.terminate()
        print("server stopped")

    server_process = None

    return server_process


def command_status_server(server_process: Optional[mp.Process]) -> None:
    """ command server status"""
    if server_process and server_process.is_alive():
        print("server is running")
    else:
        print("server is NOT running")


def command_exit_server(server_process: Optional[mp.Process]) -> None:
    """ command exit server"""
    if server_process and server_process.is_alive():
        server_process.terminate()
    print("Exiting program")


def main() -> None:
    """Main Function"""

    try:

        server_process: Optional[mp.Process] = None

        while True:

            command = input("> ")

            if command == "start":
                server_process = command_start_server(server_process)
            elif command == "stop":
                server_process = command_stop_server(server_process)
            elif command == "status":
                # step 3 - add a command named "status" that outputs to the
                # console if the server is current running or not
                # hint: follow the command function pattern used by the other
                # commands
                command_status_server(server_process)
            elif command == "exit":
                # step 4 - terminate the "server_process" if the
                # "server_process" is an object and is alive
                command_exit_server(server_process)
                break

    except KeyboardInterrupt:
        # step 5 - terminate the "server_process" if the
        # "server_process" is an object and is alive
        command_exit_server(server_process)
        pass

    sys.exit(0)


if __name__ == '__main__':
    main()
