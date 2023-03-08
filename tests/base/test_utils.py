import pytest

from shippy.base.utils import round_up_value


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
