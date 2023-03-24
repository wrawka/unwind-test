import functools
import time

from utils.logging_config import configure_logging, logging

configure_logging()


def timed_cache(seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in wrapper.cache and time.time() < wrapper.cache[cache_key][1]:
                logging.debug('Loading fom cache...')
                return wrapper.cache[cache_key][0]
            result = func(*args, **kwargs)
            wrapper.cache[cache_key] = (result, time.time() + seconds)
            return result
        wrapper.cache = {}
        return wrapper
    return decorator
