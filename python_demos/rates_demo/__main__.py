""" rates demo main """
from .get_rates import get_rates, get_rates_threaded
from .rates_api_server import rates_api_server


if __name__ == "__main__":
    # startDateStr = input("Enter start date (YYYY-mm-dd):")
    with rates_api_server():
        responseContentList = get_rates_threaded('2021-1-1')
        print("\n".join(responseContentList))
