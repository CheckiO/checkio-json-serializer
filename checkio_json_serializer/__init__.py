import json
from functools import partial

KEY_PARSE = "___checkio___type___"


def cover(name, **kwargs):
    return dict(**{KEY_PARSE: name}, **kwargs)


class CheckiOException(Exception):
    pass


class CheckiOHookException(CheckiOException):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'type "{}" is not expected'.format(self.name)


class CheckiOUnknownType(CheckiOException):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'value of type "{}" is not expected'.format(self.name)


class JSONEncoder(json.JSONEncoder):
    extra_cover = None

    def encode(self, obj, *args, **kwargs):
        return super().encode(
            obj_cover(obj, extra_cover=self.extra_cover), *args, **kwargs
        )


def obj_cover(obj, extra_cover=None):

    if extra_cover:
        for cls, name, extra_obj_cover in extra_cover:
            if isinstance(obj, cls):
                return cover(
                    name=name,
                    **extra_obj_cover(
                        obj, obj_cover=partial(obj_cover, extra_cover=extra_cover)
                    )
                )

    if isinstance(obj, list):
        return [obj_cover(v, extra_cover=extra_cover) for v in obj]
    if isinstance(obj, dict):
        return dict(
            ((k, obj_cover(v, extra_cover=extra_cover)) for k, v in obj.items())
        )
    if isinstance(obj, set):
        return cover("set", values=obj_cover(list(obj), extra_cover=extra_cover))
    if isinstance(obj, tuple):
        return cover("tuple", values=obj_cover(list(obj), extra_cover=extra_cover))
    if isinstance(obj, complex):
        return cover("complex", value=[obj.real, obj.imag])

    _module = type(obj).__module__
    if _module == "builtins":
        return obj

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

    raise CheckiOUnknownType(_name)


def object_hook(obj, extra_hooks=None):
    if KEY_PARSE in obj:
        name = obj[KEY_PARSE]
        if extra_hooks and name in extra_hooks:
            val = extra_hooks[name](obj)
        elif name == "set":
            val = set(obj["values"])
        elif name == "tuple":
            val = tuple(obj["values"])
        elif name == "complex":
            val = complex(*obj["value"])
        elif name == "decimal.Decimal":
            from decimal import Decimal

            val = Decimal(obj["value"])
        elif name == "datetime.date":
            from datetime import date

            return date(*obj["value"])
        elif name == "datetime.datetime":
            from datetime import datetime

            return datetime(*obj["value"])
        else:
            raise CheckiOHookException(name)
        return val
    return obj


def gen_object_hook(extra_hooks):
    return partial(object_hook, extra_hooks=extra_hooks)


def gen_encoder(extra_cover):
    if extra_cover is None:
        return JSONEncoder
    return type("JSONEncoder", (JSONEncoder,), {"extra_cover": extra_cover})


def dumps(*args, **kwargs):
    extra_cover = kwargs.pop("extra_cover", None)
    return json.dumps(*args, cls=gen_encoder(extra_cover), **kwargs)


def loads(*args, **kwargs):
    extra_hooks = kwargs.pop("extra_hooks", None)
    return json.loads(*args, object_hook=gen_object_hook(extra_hooks))
