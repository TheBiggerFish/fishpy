# Shamelessly stolen from https://tech.serhatteker.com/post/2019-07/python-debug-decorators/

import functools
import time
import cProfile
import io
import pstats

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

def monitor(func):
    """ Debug a method and return it back """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        
        return_value = func(*args, **kwargs)
        print(f'Calling: {func.__name__}')
        print(f'Function args: {args}, kwargs: {kwargs}')
        print(f'Function returned {return_value}')
        # logger.debug(f'Calling : {func.__name__}')
        # logger.debug(f'args, kwarg: {args, kwargs}')
        # logger.debug(f'{func.__name__} returned {return_value}')

        return return_value

    return wrapper

def timer(func):
    """ Calculate the execution time of a method and return it back """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = round(time.time() - start,6)

        print(f"Duration of {func.__name__} function was {duration}")
        # logger.debug(f"Duration of {func.__name__} function was {duration}")
        return result
    return wrapper

def profile(func):
    """ Profile the execution of a method """

    def wrapper(*args, **kwargs):
        # datafn = func.__name__ + ".profile" # Name the data file sensibly
        prof = cProfile.Profile()
        prof.enable()
        retval = func(*args,**kwargs)
        # retval = prof.runcall(func, *args, **kwargs)
        prof.disable()
        s = io.StringIO()
        ps = pstats.Stats(prof, stream=s).sort_stats('cumtime')
        ps.print_stats()
        print(s.getvalue())
        return retval
    return wrapper