""" rate server module """
from typing import Optional
import sys
import socket
import json
import re
import multiprocessing as mp
import threading
from multiprocessing.sharedctypes import Synchronized

import requests
import pyodbc
from rates_shared.rates_shared import REGEX_STING, conn_string, HOST, PORT, BASE_URL

# Use a multiprocessing shared "Value" object to track the count of
# connected clients


class ClientConnectionThread(threading.Thread):
    def __init__(self, conn: socket.socket, addr: list[str], client_count: Synchronized) -> None:
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.client_count = client_count

    def process_client_command(self, getMessage):

        matches = re.search(REGEX_STING, getMessage)

        if not matches or not matches.group('command') == "GET":
            # invalid request provided by the client
            # not in the format: GET 2019-01-03 EUR
            return "only the GET command is supported"

        date = matches.group('date')
        symbol = matches.group('symbol')

        # check database cache for date and symbol
        with pyodbc.connect(conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("select ExchangeRate \
                             from rates \
                             where ClosingDate =? and CurrencySymbol=?", (date, symbol))
                rate = cur.fetchone()
        if rate:
            # if record exists in cache
            print(f"Record {date},{symbol} FOUND in cache")
            return str(rate[0])
        else:
            # if record does not exist in chache
            print(f"Record {date},{symbol} NOT FOUND in cache")
            dateUrl = BASE_URL + date
            payload = {'base': 'USD', 'symbols': f'{symbol}'}
            responseText = requests.get(dateUrl, params=payload).text

            try:
                # handle "Invalid parameter" json response from the rest API
                responseJson = json.loads(responseText)
                responseRate = str(responseJson['rates'][symbol])
                # if valid parameters were provided to the API and got back valid response
                print(f"ADDING record {date},{symbol} to cache")
                with pyodbc.connect(conn_string) as conn:
                    conn.execute("insert into \
                                    rates (closingdate, currencysymbol, exchangerate) \
                                    values (?, ?, ?)", (date, symbol, responseRate))
            except KeyError:
                return responseText

        return responseRate

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


def command_clear_cache() -> None:
    """ command exit server"""
    print(f"CLEARING CACHE")
    with pyodbc.connect(conn_string) as conn:
        conn.execute("delete from rates;")


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
            elif command == "clear":
                # Add a command for clearing the rate cache from the server command
                # prompt. Name the command "clear".
                command_clear_cache()
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
