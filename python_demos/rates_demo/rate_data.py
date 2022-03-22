import csv
import pathlib
from typing import Any


def load_rates_from_history(rates_file_path: pathlib.Path) -> list[dict[str, Any]]:
    rates_history: dict[str, dict[str, Any]] = {}
    with open(rates_file_path, encoding="UTF-8") as rates_file:
        rates_file_csv = csv.DictReader(rates_file)
        for rate_row in rates_file_csv:
            rate_entry = {"EUR": 1.0}
            for rate_col_name, rate_col_value in rate_row.items():
                if rate_col_name == "Date":
                    row_date = rate_col_value
                else:
                    if len(rate_col_name) > 0 and rate_col_value != "N/A":
                        rate_entry[rate_col_name] = float(rate_col_value)
            rates_history[row_date] = rate_entry
    return rates_history
