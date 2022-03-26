import pyodbc
from .connections_info import conn_string

def run() -> None:
    with pyodbc.connect(conn_string) as conn:
        #rates = conn.execute("select * from rates")

        symbol = input("Input Symbol> ")
        #rates = conn.execute("select * from rates where CurrencySymbol=%(symbol)s;", {'symbol':symbol})

        rates = conn.execute("select * from rates where CurrencySymbol=?;", (symbol))

        # conn.execute("insert into rates (closingdate, currencysymbol, exchangerate) values (?, ?, ?)",
        #              (closing date, currency_symbol, exchange_rate)
        #             )

        for rate_row in rates:
            print(rate_row)

if __name__=="__main__":
    run()