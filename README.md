[![PyPI version fury.io](https://badge.fury.io/py/checkio-json-serializer.svg)](https://pypi.python.org/pypi/checkio-json-serializer/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/checkio-json-serializer.svg)](https://pypi.python.org/pypi/checkio-json-serializer/)

checkio-json-serializer
===================

## About

JSON serilizer for more complex objects

## Install

    pip install checkio-json-serializer

## Examples

Standard json module allows you to dump only limit amount of types

```python
from json import dumps

obj = set([5,4,6])

serialized_obj = dumps(obj)
```

The code above raises an exception

    TypeError: Object of type set is not JSON serializable

But if you want to be able to dump and load objects like set or datetype and use JSON format you can use checkio_json_serializer

```python
from checkio_json_serializer import dumps, loads

obj = set([5,4,6])

serialized_obj = dumps(obj)
loaded_obj = loads(serialized_obj)

assert obj == loaded_obj
``` 

## Explain

In the set example, checkio_json_serializer simply converts set-object to JSON object

`serialized_obj` variable shows

     {"___checkio___type___": "set", "values": [4, 5, 6]}

https://github.com/CheckiO/checkio-json-serializer/blob/master/tests/test_params.py contails supported datatypes

## Custom user types

checkio_json_serializer allows you to dump user-defined objects

```python
class UnexpecrtedClass:
    def __init__(self, name, param):
        self.name = name
        self.param = param

    # __hash__ and __eq__ methods for comparing objects
    # those methods are not required for using dumps or loads
    def __hash__(self):
        return hash((self.name, self.param))
    def __eq__(self, other):
        return hash(self) == hash(other)

```

In order to dump object of `UnexpecrtedClass` you need to do `extra_cover` attribute of dumps

```python
from checkio_json_serializer import dumps, loads

extra_cover = (
    (
        UnexpecrtedClass,
        lambda obj: {"values": [obj.name, obj.param]},
    ),
)

obj = {"45": UnexpecrtedClass("Alex", 200)}
serialized_obj = dumps(obj, extra_cover=extra_cover)
```

In order to load object you need to use `extra_hooks` attribute

```python
loads(serialized_obj, extra_uncover={
    "UnexpecrtedClass": lambda obj: UnexpecrtedClass(*obj["values"])
},)
```
