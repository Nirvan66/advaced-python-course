from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

import requests

from .business_days import business_days

DATE_FORMAT = "%Y-%m-%d"
BASE_URL = "http://127.0.0.1:5000/api/"
PAYLOAD = {'base': 'INR', 'symbols': 'USD,EUR'}
LOOKAHEAD_DAYS = 20


def queryServer(businessDate: str) -> str:
    formatedBusinessDate = businessDate.strftime(DATE_FORMAT)
    dateUrl = BASE_URL + formatedBusinessDate
    payload = PAYLOAD
    return requests.get(dateUrl, params=payload).text


def get_rates(startDateStr: str) -> list[str]:
    startDate = datetime.strptime(startDateStr, DATE_FORMAT).date()
    endDate = startDate + timedelta(LOOKAHEAD_DAYS)
    responseContentList = list(map(lambda x: queryServer(x),
                                   business_days(startDate, endDate)))
    return responseContentList


def get_rates_threaded(startDateStr: str) -> list[str]:
    startDate = datetime.strptime(startDateStr, DATE_FORMAT).date()
    endDate = startDate + timedelta(LOOKAHEAD_DAYS)
    with ThreadPoolExecutor() as excecutor:
        responseContentList = list(excecutor.map(queryServer,
                                                 business_days(startDate,
                                                               endDate)))
    return responseContentList
