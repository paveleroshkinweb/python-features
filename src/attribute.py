from functools import partial


def attr(obj, prop, default=None):
    if isinstance(obj, dict):
        return obj[prop]

    if hasattr(obj, '__dict__') and prop in obj.__dict__:
        return obj.__dict__[prop]

    for cl in type(obj).mro():
        if prop in cl.__dict__:
            if callable(cl.__dict__[prop]):
                if isinstance(obj, type):
                    return cl.__dict__[prop]
                return partial(cl.__dict__[prop], obj)
            return cl.__dict__[prop]
    return default
