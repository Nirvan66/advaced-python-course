from datetime import timedelta, date
from collections.abc import Generator
import holidays

COUNTRY = "US"


def business_days(startDate: date, endDate: date) -> Generator[date, None, None]:
    usHolidays = holidays.country_holidays(COUNTRY)
    currentDate = startDate
    while currentDate <= endDate:
        weekday = currentDate.weekday()
        if weekday < 5 and currentDate not in usHolidays:
            yield currentDate
        currentDate += timedelta(days=1)
