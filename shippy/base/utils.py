import math
from datetime import datetime

from dateutil.rrule import DAILY, FR, MO, TH, TU, WE, rrule


def round_up_value(val: float, decimals: int = 1):
    return math.ceil(val * 10 * decimals) / 10 * decimals


def get_date_after_n_workdays(
    days: int, start_datetime: datetime = datetime.now()
) -> datetime:
    return rrule(freq=DAILY, dtstart=start_datetime, byweekday=(MO, TU, WE, TH, FR))[days]
