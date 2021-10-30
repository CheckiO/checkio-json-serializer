checkio-json-serializer
===================

## About

JSON serilizer for more complex objects

## Examples

```python
from checkio_json_serializer import dumps, loads

obj = set([5,4,6])

serialized_obj = dumps(obj)
loaded_obj = loads(obj)

assert obj == loaded_obj
``` 
