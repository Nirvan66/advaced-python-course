""" rates demo main """
from .get_rates import get_rates


if __name__ == "__main__":
    responseContentList = get_rates()
    print("\n".join(responseContentList))
