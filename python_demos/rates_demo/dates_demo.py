from datetime import date, datetime, timedelta
import time

def run_demo() -> None:
    current_time = time.time()

    print(current_time)

    start = datetime.now()
    end = start + timedelta(days=180)

    print(start)
    print(end)
    print(type(start))
    print(type(timedelta(days=180)))
