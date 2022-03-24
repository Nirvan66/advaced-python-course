""" rate server module """
from typing import Optional
from contextlib import contextmanager
from collections.abc import Generator
import sys
import socket

import multiprocessing as mp
import threading
from multiprocessing.sharedctypes import Synchronized
from urllib import response
import requests
import json
import re

HOST = "127.0.0.1"
PORT = 5075
BASE_URL = "http://127.0.0.1:5000/api/"

REGEX_STING= r"^(?P<command>\w+)\s(?P<date>\d{4}-\d{1,2}-\d{1,2})\s(?P<symbol>\w+)"
REGEX_COMPILED = re.compile(REGEX_STING)

# Use a multiprocessing shared "Value" object to track the count of
# connected clients


class ClientConnectionThread(threading.Thread):
    def __init__(self, conn: socket.socket, addr: list[str], client_count: Synchronized) -> None:
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.client_count = client_count

    def process_client_command(self, getMessage):

        regex= r"^(?P<command>\w+)\s(?P<date>\d{4}-\d{1,2}-\d{1,2})\s(?P<symbol>\w+)"
        matches= re.search(regex, getMessage)

        if not matches or not matches.group('command')=="GET":
            # invalid request provided by the client
            # not in the format: GET 2019-01-03 EUR
            return "only the GET command is supported"

        date =  matches.group('date')
        symbol = matches.group('symbol')

        dateUrl = BASE_URL + date
        payload = {'base': 'USD', 'symbols': f'{symbol}'}
        responseText = requests.get(dateUrl, params=payload).text

        try:
            # handle "Invalid parameter" json response from the rest API
            responseJson = json.loads(responseText)
            return str(responseJson['rates'][symbol])
        except KeyError:
            return responseText

    def run(self) -> None:
        """ Target function of thread. Listens for messages from a single client"""
        # increment the count when a client connects, and decrement the count when
        # a client disconnects
        with self.client_count.get_lock():
            self.client_count.value += 1

        print(f"Client at {self.addr[0]}:{self.addr[1]}, ",
              "connected to the Rate Server")
        self.conn.sendall(f"Welcome to {HOST}:{PORT}".encode())
        # wire up an echo server which receives a string and echos back to
        while True:
            message = self.conn.recv(2048).decode()
            if not message:
                break

            print(f"recv: {message}")
            ratesApiOutput = self.process_client_command(message)
            self.conn.sendall(ratesApiOutput.encode())

        with self.client_count.get_lock():
            self.client_count.value -= 1
        print("We've lost a client y'all")


def rate_server(host: str, port: int, client_count: Synchronized) -> None:
    """rate server"""
    # implement socket server
    # the host and port should be received as parameters into this function
    # use "AF_INET" for IPv4
    # use "SOCK_STREAM" for TCP
    # when a client connects, send the following string:
    # "Connected to the Rate Server"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        socket_server.bind((host, port))
        socket_server.listen()
        print(f"server is listening on {host}:{port}")
        while True:
            # blocking call waiting for client to connect
            conn, addr = socket_server.accept()
            print(type(conn))
            clientConnectionThread = ClientConnectionThread(
                conn, addr, client_count)
            clientConnectionThread.start()


def command_start_server(server_process: Optional[mp.Process], client_count: Synchronized) -> mp.Process:
    """ command start server """

    if server_process and server_process.is_alive():
        print("server is already running")
    else:
        # step 1 - create a new process object
        server_process = mp.Process(
            target=rate_server, args=(HOST, PORT, client_count))
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


def command_count_server(client_count: Synchronized) -> None:
    """ command exit server"""
    print(f"There are {client_count.value} clients connected")


def main() -> None:
    """Main Function"""

    try:

        server_process: Optional[mp.Process] = None
        client_count: Synchronized = mp.Value('i', 0)

        while True:

            command = input("> ")

            if command == "start":
                server_process = command_start_server(
                    server_process, client_count)
            elif command == "stop":
                server_process = command_stop_server(server_process)
            elif command == "count":
                # add a new server command named "count" that displays the count of
                # connected clients
                command_count_server(client_count)
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
