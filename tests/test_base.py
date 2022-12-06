import json
import pytest
from copy import deepcopy
from checkio_json_serializer import (
    dumps,
    KEY_PARSE,
    loads,
    object_uncover,
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


def test_loads_wrong_name():
    """
    unexpected key will be simply skiped
    """
    assert loads(json.dumps({"a": {KEY_PARSE: "unknown_dict", "values": [4, 5]}})) == {
        "a": {KEY_PARSE: "unknown_dict", "values": [4, 5]}
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
    with pytest.raises(TypeError):
        dumps(CUSTOM_OBJ)


def test_dumps_extra():
    """
    Use extra_cover for submiting custom objects
    """
    extra_cover = (
        (
            UnexpecrtedClass,
            lambda obj: {"values": [obj.name, obj.param]},
        ),
    )
    assert (
        json.loads(dumps(CUSTOM_OBJ, extra_cover=extra_cover)) == SERIALIZED_CUSTOM_OBJ
    )


def test_loads_extra():
    """
    Use extra_uncover for parsing complex objects
    """
    assert (
        loads(
            json.dumps(SERIALIZED_CUSTOM_OBJ),
            extra_uncover={
                "UnexpecrtedClass": lambda obj: UnexpecrtedClass(*obj["values"])
            },
        )
        == CUSTOM_OBJ
    )


def test_nested_user_object():
    val = {
        "45": UnexpecrtedClass("Alex", 200),
        "Mix": UnexpecrtedClass("Alex", UnexpecrtedClass("Mike", 100)),
    }
    extra_uncover = {"UnexpecrtedClass": lambda obj: UnexpecrtedClass(*obj["values"])}
    extra_cover = (
        (
            UnexpecrtedClass,
            lambda obj: {"values": [obj.name, obj.param]},
        ),
    )
    assert val == loads(
        dumps(val, extra_cover=extra_cover), extra_uncover=extra_uncover
    )


def test_dumps_extra_overwrite_name():
    """
    Use extra_cover for submiting custom objects
    """
    extra_cover = (
        (UnexpecrtedClass, lambda obj: {"values": [obj.name, obj.param]}, "important"),
    )
    extra_uncover = {"important": lambda obj: UnexpecrtedClass(*obj["values"])}

    dump_val = {"45": {KEY_PARSE: "important", "values": ["Alex", 200]}}
    assert json.loads(dumps(CUSTOM_OBJ, extra_cover=extra_cover)) == dump_val

    assert loads(json.dumps(dump_val), extra_uncover=extra_uncover) == CUSTOM_OBJ


def test_object_unchanged():
    result = {KEY_PARSE: "set", "values": [2, 3]}
    result_copy = deepcopy(result)
    result_value = object_uncover(result)

    assert result_value == {2, 3}
    assert result == result_copy


def test_iterable():
    assert dumps({"a": 1, "b": 2}.values()) == "[1, 2]"
