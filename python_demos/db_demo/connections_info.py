docker_conn_options = [
    "DRIVER={ODBC Driver 17 for SQL Server}",
    "SERVER=localhost,1433",
    "DATABASE=ratesapp",
    "UID=sa",
    "PWD=sqlDbp@ss!",
]


conn_string = ';'.join(docker_conn_options)

# docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=sqlDbp@ss!" -e "MSSQL_PID=Express" -p 1433:1433 -d mcr.microsoft.com/mssql/server:2019-latest

# sa

# docker ps

# docker logs <>