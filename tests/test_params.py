import pytest
from checkio_json_serializer import dumps, loads
from decimal import Decimal
from datetime import date, datetime

ALL = [
    # 1 set
    {"a": set([4, 5])},

    # 2 tuple
    ("5", "6", 89),

    # 3 nested types
    ("5", "6", (8, 9)),

    # 4 different kind of nested values
    ("5", ("6", set([5, 6, 7]), (8, 9))),

    # 5 simple type - str
    "56",

    # 6 simple type = int
    78,

    # 7 Decimal
    [Decimal("3.4"), Decimal("-200"), "56", 89],

    # 8 comples
    {"678": complex(6, 8)},

    # 9 datetime and date
    (datetime(2021, 10, 30, 15, 18, 24, 599340), date(2020, 2, 5)),
]


@pytest.mark.parametrize("val", ALL)
def test_all(val):
    assert val == loads(dumps(val))
