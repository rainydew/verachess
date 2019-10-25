# coding: utf-8
from verachess_global import Globals, ModelLock
from functools import wraps


def check_model(func):
    # return type should be None
    @wraps(func)
    def inner_func(*args, **kwargs):
        if not Globals.Models:
            func(*args, **kwargs)
    return inner_func


def model_locked(func):
    # use modelLock at a function
    @wraps(func)
    def inner_func(*args, **kwargs):
        if Globals.Models:
            # cannot acquire model lock
            return None
        with ModelLock():
            return func(*args, **kwargs)
    return inner_func
