import json
import pytest
from checkio_json_serializer import (
    dumps,
    KEY_PARSE,
    loads,
    CheckiOHookException,
    CheckiOUnknownType,
)


def test_dumps():
    assert json.loads(dumps({"a": set([4, 5])})) == {
        "a": {KEY_PARSE: "set", "values": [4, 5]}
    }


def test_loads():
    assert loads(json.dumps({"a": {KEY_PARSE: "set", "values": [4, 5]}})) == {
        "a": set([4, 5])
    }


def test_exception_simple_key():
    with pytest.raises(TypeError):
        dumps({(1, 2): 3})


def test_exception_loads_wrong_name():
    with pytest.raises(CheckiOHookException):
        loads(json.dumps({"a": {KEY_PARSE: "unknown_dict", "values": [4, 5]}})) == {
            "a": set([4, 5])
        }


class UnexpecrtedClass:
    def __init__(self, name, param):
        self.name = name
        self.param = param

    def __hash__(self):
        return hash((self.name, self.param))

    def __eq__(self, other):
        return hash(self) == hash(other)


def test_exception_unexpected_type_value():
    with pytest.raises(CheckiOUnknownType):
        dumps({"45": UnexpecrtedClass("Alex", 200)})


def test_dumps_extra():
    extra_cover = (
        (
            UnexpecrtedClass,
            "UnexpecrtedClass",
            lambda obj, obj_cover: {"values": [obj.name, obj.param]},
        ),
    )
    assert json.loads(
        dumps({"45": UnexpecrtedClass("Alex", 200)}, extra_cover=extra_cover)
    ) == {"45": {KEY_PARSE: "UnexpecrtedClass", "values": ["Alex", 200]}}


def test_loads_extra():
    assert (
        loads(
            json.dumps(
                {"45": {KEY_PARSE: "UnexpecrtedClass", "values": ["Alex", 200]}}
            ),
            extra_hooks={
                "UnexpecrtedClass": lambda obj: UnexpecrtedClass(*obj["values"])
            },
        )
        == {"45": UnexpecrtedClass("Alex", 200)}
    )
