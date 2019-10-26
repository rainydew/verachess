# coding: utf-8
from verachess_global import Globals, ModelLock
from functools import wraps
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')


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
            logging.warning("cannot acquire model lock")
            return None
        with ModelLock():
            return func(*args, **kwargs)
    return inner_func
