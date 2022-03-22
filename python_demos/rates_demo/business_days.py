from datetime import timedelta, datetime, date
from collections.abc import Generator
import holidays

DATE_FORMAT = "%m/%d/%Y"
COUNTRY = "US"

def business_days(startDate: str, endDate: str) -> Generator[date, None, None]:
    startDate = datetime.strptime(startDate, DATE_FORMAT).date()
    endDate = datetime.strptime(endDate, DATE_FORMAT).date()
    
    usHolidays = holidays.country_holidays(COUNTRY)
    currentDate = startDate
    while currentDate <= endDate:
        weekday = currentDate.weekday()
        if weekday<5 and currentDate not in usHolidays:
            yield currentDate
        currentDate += timedelta(days=1)
