from typing import Any
from urllib import response
from flask import Flask, Response, request, abort, jsonify
from rates_demo.rate_data import load_rates_from_history
import pathlib

app = Flask(__name__)

rates: dict[str,dict[str, Any]] = {}

@app.route("/")
def home() -> Response:
    return "<h1>Hello, World!</h1>"

@app.route("/check")
def check() -> Response:
    return "READY"

@app.route("/api/<rate_date>")
def getDates(rate_date: str) ->  Response:
    """ get rates data from locally loaded csv"""
    rates_by_country = rates.get(rate_date, None)
    response_dict = {"Invalid Parameters": "Ya Nucklehead"}
    if rates_by_country:
        base_country = request.args.get('base', "EUR")
        country_codes = request.args.get('symbols', '').split(',')

        rates_by_country_codes = {country_code: rates_by_country[country_code]
                                for country_code in country_codes 
                                if country_code in rates_by_country}
        base_country_rate = rates_by_country.get(base_country, None)

        if base_country_rate is None:
            response_dict = {"Invalid Parameters": f"base country rate not found for {base_country}"}
        elif len(rates_by_country_codes)==0:
            response_dict = {"Invalid Parameters": "no country symbols provided"}
        else:
            # valid parameters
            country_rates = {country_code: country_rate/base_country_rate
            for (country_code, country_rate) in rates_by_country_codes.items()}
            response_dict = {
                "date": rate_date,
                "base": base_country,
                "rates": country_rates
            }
    else:
        response_dict = {"Invalid Parameters": f"no data found for date {rate_date}"}
    
    return jsonify(response_dict)

def start_rates_api() -> None:
    global rates

    rates_file_path = pathlib.Path("..", "data", "eurofxref-hist.csv")

    rates = load_rates_from_history(rates_file_path)
    app.run()

if __name__=="__main__":
    start_rates_api()