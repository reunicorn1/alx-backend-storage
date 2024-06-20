#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import requests
from functools import wraps
import redis
from typing import Callable, Any


def cache_pages(method: Callable) -> Callable:
    """
    This is a decorator that caches results and return it from the
    database if it's still available

    Parameters:
    ----------
    url: str
    result: str

    Returns:
    --------
    the wrapper function
    """
    @wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        """
        returns the results from the cache or stores it
        """
        cache = redis.Redis(host='127.0.0.1', port=6379)
        result = cache.get(str(args))
        if not result:
            result = method(*args)
            cache.setex(str(args), 10, result)
        return result
    return wrapper


def count_occurance(method: Callable) -> Callable:
    """
    This is a decorator that tracks how many times a particular URL
    was accessed in the key "count:{url}"

    Parameters:
    ----------
    url: str
    result: str

    Returns:
    --------
    the wrapper function
    """
    @wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        """
        returns the results from the cache or stores it
        """
        cache = redis.Redis(host='127.0.0.1', port=6379)
        cache.incr('count:{}'.format(args[0]))
        return method(*args, **kwargs)
    return wrapper


@count_occurance
@cache_pages
def get_page(url: str) -> str:
    """
    This function uses the requests module to obtain the HTML content
    of a particular URL and returns it.

    Parameters:
    ----------
    url: str
        A url to be used to obtain the HTML content

    Returns:
        The HTML content of the page
    """
    response = requests.get(str(url))
    if response.status_code == 200:
        return response.text
    return '(nil)'
