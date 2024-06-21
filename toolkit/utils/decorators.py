from functools import wraps
import warnings
from .context_manager import Timer


def return_string(keys):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            res = func(*args, **kwargs)
            assert len(res) == len(keys)
            
            s = ""
            for key, r in zip(keys, res):
                s += "{}: {}\t".format(key, r)
            return s
        return wrapped_function
    return decorator


def printable(key=None, confirm=True):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            result = func(*args, **kwargs)
            if confirm:
                if key:
                    msg = "[{}]: [{}]".format(key, result)
                else:
                    msg = "[{}]".format(result)
                print(msg)
            return result
        return wrapped_function
    return decorator


def deprecated(reason=None, new=None):
    def decorator(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            message = "Call to deprecated function '{}'.".format(func.__name__)
            if reason:
                message += "\nThis method is deprecated now because of '{}'".format(reason)
            if new:
                message += "\nUse '{}' instead.".format(new)
            warnings.warn(message,
                          category=DeprecationWarning,
                          stacklevel=2)
            return func(*args, **kwargs)
        return new_func
    return decorator


def verbose(task):
    def decorator(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            with Timer(task, verbose=args[0].verbose):
                res = func(*args, **kwargs)
            print("{}: {}".format(task, res))
            return res
        return new_func
    return decorator