import pytest
from checkio_json_serializer import dumps, loads
from decimal import Decimal
from datetime import date, datetime

ALL = [
    # 1
    {"a": set([4, 5])},
    # 2
    ("5", "6", 89),
    # 3
    ("5", "6", (8, 9)),
    # 4
    ("5", ("6", set([5, 6, 7]), (8, 9))),
    # 5
    "56",
    # 6
    78,
    # 7
    [Decimal("3.4"), Decimal("-200"), "56", 89],
    # 8
    {"678": complex(6, 8)},
    # 9
    (datetime(2021, 10, 30, 15, 18, 24, 599340), date(2020, 2, 5)),
]


@pytest.mark.parametrize("val", ALL)
def test_all(val):
    assert val == loads(dumps(val))
