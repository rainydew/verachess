# coding: utf-8
import time


def today():
    return time.strftime("%Y-%m-%d", time.localtime())


def now():
    return time.strftime("%H:%M:%S", time.localtime())


if __name__ == '__main__':
    print(now())
