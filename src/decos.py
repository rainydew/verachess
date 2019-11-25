# coding: utf-8
from verachess_global import Globals, ModelLock
from functools import wraps
from traceback import format_exc
from tooltip import alert
import logging


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
            alert("你有弹出窗口未关闭，暂不能使用此功能")
            return None
        with ModelLock():
            return func(*args, **kwargs)
    return inner_func


def none_trier(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logging.warning(format_exc())
            return None
    return inner_func
