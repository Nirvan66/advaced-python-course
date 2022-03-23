""" rates demo main """
from .get_rates import get_rates, get_rates_threaded
from .rates_api_server import rates_api_server


if __name__ == "__main__":
    # startDateStr = input("Enter start date (YYYY-mm-dd):")

    # fires up server in the context manager on separate process
    with rates_api_server():
        # client can make request to server running on separate process
        responseContentList = get_rates_threaded('2021-1-1')
        print("\n".join(responseContentList))
    # runs all code after yield in the context manager
