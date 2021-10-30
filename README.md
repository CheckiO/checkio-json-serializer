checkio-json-serializer
===================

## About

JSON serilizer for more complex objects

## Install

    pip install checkio-json-serializer

## Examples

```python
from checkio_json_serializer import dumps, loads

obj = set([5,4,6])

serialized_obj = dumps(obj)
loaded_obj = loads(serialized_obj)

assert obj == loaded_obj
``` 
