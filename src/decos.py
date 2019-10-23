# coding: utf-8
from verachess_global import Globals
from functools import wraps

def check_model(func):
    # return type should be None
    @wraps(func)
    def inner_func(*args, **kwargs):
        if not Globals.Models:
            func(*args, **kwargs)
    return inner_func