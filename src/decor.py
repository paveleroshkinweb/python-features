import time
from collections import namedtuple


def wraps(original_fn):

    def outer(fn):

        def inner(*args, **kwargs):
            return fn(*args, **kwargs)

        inner.__name__ = original_fn.__name__
        inner.__doc__ = original_fn.__doc__
        inner.__module__ = original_fn.__module__
        inner.__dict__ = { **original_fn.__dict__ }
        return inner

    return outer


def once(f):
    
    called = False

    @wraps(f)
    def inner(*args, **kwargs):
        nonlocal called
        if not called:
            result = f(*args, **kwargs)
            called = True
            return result

    return inner


def profile(fn):

    @wraps(fn)
    def inner(*args, **kwargs):
        result = None
        err = None
        try:
            start = time.perf_counter()
            result = fn(*args, **kwargs)
        except Exception as e:
            err = e
        finally:
            diff = time.perf_counter() - start
            inner.__calls__ += 1
            inner.__time__ += diff
            if err:
                raise err
            return result 

    inner.__calls__ = 0
    inner.__time__ = 0
    return inner
