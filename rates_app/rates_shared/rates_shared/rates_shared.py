import re

HOST = "127.0.0.1"
PORT = 5075
BASE_URL = "http://127.0.0.1:5000/api/"

docker_conn_options = [
    "DRIVER={ODBC Driver 17 for SQL Server}",
    "SERVER=localhost,1433",
    "DATABASE=ratesapp",
    "UID=sa",
    "PWD=sqlDbp@ss!",
]

conn_string = ";".join(docker_conn_options)

REGEX_STING = r"^(?P<command>\w+)\s(?P<date>\d{4}-\d{1,2}-\d{1,2})\s(?P<symbol>\w+)"
REGEX_COMPILED = re.compile(REGEX_STING)