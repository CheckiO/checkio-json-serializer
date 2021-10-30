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
    """
    JSON can only use simple types for key
    """
    with pytest.raises(TypeError):
        dumps({(1, 2): 3})


def test_exception_loads_wrong_name():
    with pytest.raises(CheckiOHookException):
        loads(json.dumps({"a": {KEY_PARSE: "unknown_dict", "values": [4, 5]}})) == {
            "a": set([4, 5])
        }


class UnexpecrtedClass:
    """
    Example of non-builtoin class.

    Methods __hash__ and __eq__ are for compering test results
    """

    def __init__(self, name, param):
        self.name = name
        self.param = param

    def __hash__(self):
        return hash((self.name, self.param))

    def __eq__(self, other):
        return hash(self) == hash(other)


CUSTOM_OBJ = {"45": UnexpecrtedClass("Alex", 200)}
SERIALIZED_CUSTOM_OBJ = {"45": {KEY_PARSE: "UnexpecrtedClass", "values": ["Alex", 200]}}


def test_exception_unexpected_type_value():
    """
    You can't serialize any object custom object
    """
    with pytest.raises(CheckiOUnknownType):
        dumps(CUSTOM_OBJ)


def test_dumps_extra():
    """
    Use extra_cover for submiting custom objects
    """
    extra_cover = (
        (
            UnexpecrtedClass,
            "UnexpecrtedClass",
            lambda obj, obj_cover: {"values": [obj.name, obj.param]},
        ),
    )
    assert (
        json.loads(dumps(CUSTOM_OBJ, extra_cover=extra_cover)) == SERIALIZED_CUSTOM_OBJ
    )


def test_loads_extra():
    """
    Use extra_hooks for parsing complex objects
    """
    assert (
        loads(
            json.dumps(SERIALIZED_CUSTOM_OBJ),
            extra_hooks={
                "UnexpecrtedClass": lambda obj: UnexpecrtedClass(*obj["values"])
            },
        )
        == CUSTOM_OBJ
    )
