from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import threading

import requests

from .business_days import business_days

DATE_FORMAT = "%Y-%m-%d"
BASE_URL = "http://127.0.0.1:5000/api/"
PAYLOAD = {'base': 'INR', 'symbols': 'USD,EUR'}
LOOKAHEAD_DAYS = 20


def queryServerPool(businessDate: str) -> str:
    """used for thread pool"""
    formatedBusinessDate = businessDate.strftime(DATE_FORMAT)
    dateUrl = BASE_URL + formatedBusinessDate
    payload = PAYLOAD
    return requests.get(dateUrl, params=payload).text


def get_rates_threaded_pool(startDateStr: str) -> list[str]:
    startDate = datetime.strptime(startDateStr, DATE_FORMAT).date()
    endDate = startDate + timedelta(LOOKAHEAD_DAYS)
    with ThreadPoolExecutor() as excecutor:
        responseContentList = list(excecutor.map(queryServerPool,
                                                 business_days(startDate,
                                                               endDate)))
    return responseContentList


def queryServerThread(businessDate: str, responseContentList: list[str]) -> str:
    """used for single thread"""
    formatedBusinessDate = businessDate.strftime(DATE_FORMAT)
    dateUrl = BASE_URL + formatedBusinessDate
    payload = PAYLOAD
    responseContentList.append(requests.get(dateUrl, params=payload).text)


def get_rates_threaded(startDateStr: str) -> list[str]:
    startDate = datetime.strptime(startDateStr, DATE_FORMAT).date()
    endDate = startDate + timedelta(LOOKAHEAD_DAYS)

    responseContentList: list[str] = []
    threads: list[threading.Thread] = []

    for businessDate in business_days(startDate, endDate):
        a_thread = threading.Thread(target=queryServerThread,
                                    args=(businessDate, responseContentList,))
        a_thread.start()
        threads.append(a_thread)

    for a_thread in threads:
        a_thread.join()

    return responseContentList


def get_rates(startDateStr: str) -> list[str]:
    startDate = datetime.strptime(startDateStr, DATE_FORMAT).date()
    endDate = startDate + timedelta(LOOKAHEAD_DAYS)
    responseContentList = list(map(lambda x: queryServerPool(x),
                                   business_days(startDate, endDate)))
    return responseContentList
