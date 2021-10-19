"""This module contains function decorators to use in debugging"""

# Shamelessly stolen from https://tech.serhatteker.com/post/2019-07/python-debug-decorators/

import cProfile
import functools
import io
import pstats
import time
from typing import Callable


def monitor(func):
    """ Debug a method, printing inputs and ouputs """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return_value = func(*args, **kwargs)
        print(f'Calling: {func.__name__}')
        print(f'Function args: {args}, kwargs: {kwargs}')
        print(f'Function returned {return_value}')
        return return_value
    return wrapper

def log(log_function:Callable[[str],None]=print):
    """ Debug a method and output using log_function """
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            return_value = function(*args, **kwargs)
            log_function(f'Calling: {function.__name__}')
            log_function(f'Function args: {args}, kwargs: {kwargs}')
            log_function(f'Function returned: {return_value}')
            return return_value
        return wrapper
    return decorator

def timer(func):
    """ Calculate the execution time of a method and return it back """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = round(time.time() - start,6)
        print(f'Duration of {func.__name__} function was {duration}')
        return result
    return wrapper

def profile(func):
    """ Profile the execution of a method """
    def wrapper(*args, **kwargs):
        prof = cProfile.Profile()
        prof.enable()
        retval = func(*args,**kwargs)
        prof.disable()
        stream = io.StringIO()
        stats = pstats.Stats(prof, stream=stream).sort_stats('cumtime')
        stats.print_stats()
        print(stream.getvalue())
        return retval
    return wrapper
