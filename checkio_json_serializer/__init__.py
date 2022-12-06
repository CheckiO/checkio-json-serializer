import json
from functools import partial
from copy import deepcopy
from collections.abc import Iterable

KEY_PARSE = "___checkio___type___"


def cover(name, **kwargs):
    return dict(**{KEY_PARSE: name}, **kwargs)


class JSONEncoder(json.JSONEncoder):
    extra_cover = None

    def encode(self, obj, *args, **kwargs):
        return super().encode(
            object_cover(obj, extra_cover=self.extra_cover), *args, **kwargs
        )


def object_cover(obj, extra_cover=None):
    """
    function that converts non-JSON-serializable python object into JSON-serializable

    @extra_cover for convering custom objects - is a list of lists of 3 elements. (CustomClass, unique name, and function for converting)
    """

    if extra_cover:
        for cls, extra_object_cover, *other in extra_cover:
            name = other[0] if other else cls.__name__
            if isinstance(obj, cls):
                return cover(
                    name=name,
                    **dict(
                        (
                            (k, object_cover(v, extra_cover=extra_cover))
                            for k, v in extra_object_cover(obj).items()
                        )
                    )
                )

    if isinstance(obj, list):
        return [object_cover(v, extra_cover=extra_cover) for v in obj]
    if isinstance(obj, dict):
        return dict(
            ((k, object_cover(v, extra_cover=extra_cover)) for k, v in obj.items())
        )
    if isinstance(obj, set):
        return cover("set", values=object_cover(list(obj), extra_cover=extra_cover))
    if isinstance(obj, tuple):
        return cover("tuple", values=object_cover(list(obj), extra_cover=extra_cover))
    if isinstance(obj, complex):
        return cover("complex", value=[obj.real, obj.imag])

    _module = type(obj).__module__
    _name = _module + "." + type(obj).__name__
    _cover = partial(cover, _name)

    if _name == "decimal.Decimal":
        return _cover(value=str(obj))
    if _name == "datetime.date":
        return _cover(value=[obj.year, obj.month, obj.day])
    if _name == "datetime.datetime":
        return _cover(
            value=[
                obj.year,
                obj.month,
                obj.day,
                obj.hour,
                obj.minute,
                obj.second,
                obj.microsecond,
            ]
        )

    if isinstance(obj, str):
        return obj

    if isinstance(obj, Iterable):
        return [object_cover(v, extra_cover=extra_cover) for v in obj]

    return obj


def object_uncover(obj, extra_uncover=None, skip_key_parse=False):
    """
    Function that object into non-JSON-serializable python object

    @extra_uncover for parsing custom objects - a dict where key is a unique name and value is converting function.
    """
    if not skip_key_parse and isinstance(obj, dict) and KEY_PARSE in obj:
        name = obj[KEY_PARSE]
        obj = object_uncover(obj, extra_uncover=extra_uncover, skip_key_parse=True)
        if extra_uncover and name in extra_uncover:
            return extra_uncover[name](obj)
        elif name == "set":
            return set(obj["values"])
        elif name == "tuple":
            return tuple(obj["values"])
        elif name == "complex":
            return complex(*obj["value"])
        elif name == "decimal.Decimal":
            from decimal import Decimal

            return Decimal(obj["value"])
        elif name == "datetime.date":
            from datetime import date

            return date(*obj["value"])
        elif name == "datetime.datetime":
            from datetime import datetime

            return datetime(*obj["value"])
        else:
            return obj

    if isinstance(obj, dict):
        return dict(
            (
                (k, object_uncover(v, extra_uncover=extra_uncover))
                for k, v in obj.items()
            )
        )

    if isinstance(obj, list):
        return [object_uncover(v, extra_uncover=extra_uncover) for v in obj]

    return obj


def gen_encoder(extra_cover):
    if extra_cover is None:
        return JSONEncoder
    return type("JSONEncoder", (JSONEncoder,), {"extra_cover": extra_cover})


def dumps(*args, **kwargs):
    extra_cover = kwargs.pop("extra_cover", None)
    return json.dumps(*args, cls=gen_encoder(extra_cover), **kwargs)


def loads(*args, **kwargs):
    extra_uncover = kwargs.pop("extra_uncover", None)
    obj = json.loads(*args, **kwargs)
    return object_uncover(obj, extra_uncover=extra_uncover)
