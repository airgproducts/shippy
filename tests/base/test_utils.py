from datetime import datetime

import pytest

from shippy.base.utils import get_date_after_n_workdays, round_up_value


@pytest.mark.parametrize(
    "value,expected",
    [
        (2.2, 2.2),
        (1.0, 1.0),
        (2.99, 3.0),
        (2.98, 3.0),
        (2.90, 2.9),
        (2.91, 3),
        (1.11, 1.2),
        (1.0, 1.0),
        (1.10, 1.10),
        (12.34, 12.4),
        (12.01, 12.1),
        (12.0001, 12.1),
    ],
)
def test_round_up_value(value, expected):
    assert round_up_value(value) == expected


@pytest.mark.parametrize(
    "start_date,days,expected_result",
    [
        (datetime(year=2023, month=3, day=15), 1, datetime(year=2023, month=3, day=16)),
        (datetime(year=2023, month=3, day=15), 3, datetime(year=2023, month=3, day=20)),
        (datetime(year=2023, month=3, day=15), 10, datetime(year=2023, month=3, day=29)),
    ],
)
def test_get_date_after_n_workdays(start_date, days, expected_result):
    assert (
        get_date_after_n_workdays(days=days, start_datetime=start_date) == expected_result
    )
