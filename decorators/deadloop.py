# -*- coding: utf-8 -*-

__all__ = ['deadloop']

import functools
import threading


# a wrapper to execute a function in deadloop
# until the given event is set. sleep interval beteen each loop.
def deadloop(event, interval):
    def wrapper(func):
        """ Execute `func` in dead loop until `event` is set,

            @event:     deadloop's breaking event;
            @interval:  loop sleep seconds, non-negative.
        """
        assert isinstance(event, threading._Event)
        assert isinstance(interval, (int, long, float)) and interval >= 0.0

        @functools.wraps(func)
        def routine(*args, **kwargs):
            while 1:
                func(*args, **kwargs)

                event.wait(timeout=interval)
                if event.is_set():
                    break
        return routine
    return wrapper

