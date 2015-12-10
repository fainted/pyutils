# -*- coding: utf-8 -*-

__all__ = ['timecost']


import functools
import time

def timecost(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Set functions execution costs, which is
           in milliseconds as the last return value.
        """
        start = time.time()

        return func(*args, **kwargs), int(1000 * (time.time() - start))
    return wrapper


if __name__ == '__main__':
    @timecost
    def foo(interval):
        time.sleep(interval)

    print(foo(4.20))
    print(foo(5.80))

