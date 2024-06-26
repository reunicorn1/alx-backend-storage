#!/usr/bin/env python3
"""
Redis basic
"""
import asyncio
import inspect
from functools import wraps
import redis
from typing import Union, Callable, Any, Tuple, Dict, Iterable
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """
    This is a decorator function that counts the number of times
    a certain Cache method was called

    Parameters:
    ----------
    method: Callable

    Returns:
    -------
        the wrapper function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        This is a wrapper function that calls incby to keep count
        of the t()mes a certain function was called
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    This is a decorator function that stores the history of inputs and
    outputs for a particular function

    Parameters:
    ----------
    method: Callable

    Returns:
    -------
        the wrapper function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        This is a wrapper function that adds additional actions during
        the execution of the argument function
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush('{}:inputs'.format(method.__qualname__),
                              str(args))
            result = method(self, *args, **kwargs)
            self._redis.rpush('{}:outputs'.format(method.__qualname__),
                              result)
        return result
    return wrapper


def replay(method):
    """
    This function displays the history of calls of a particular
    function

    Parameters:
    ----------
    method: a Callable

    Returns:
        None
    """
    if isinstance(method.__self__._redis, redis.Redis):
        cache = method.__self__._redis
        inn = cache.lrange('{}:inputs'.format(method.__qualname__), 0, -1)
        out = cache.lrange('{}:outputs'.format(method.__qualname__), 0, -1)
        print('{} was called {} times:'.format(method.__qualname__, len(out)))
        for i, j in zip(inn, out):
            print('{}(*{}) -> {}'.format(method.__qualname__,
                                         i.decode('utf-8'),
                                         j.decode('utf-8')))


class Cache:
    """
    A class to represent a cache storage engine
    ...

    Attributes
    ----------
    TBD

    Methods
    -------
    store(data: str, bytes, int, float):
        takes a data argument generates a random key using uuid
        and stores the input data and returns the key
    """

    def __init__(self):
        """
        Constructs all necessary attributes for the cache object.
        """
        self._redis = redis.Redis(host='127.0.0.1', port=6379)
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        takes a data argument generates a random key using uuid
        and stores the input data and returns the key

        Parameters:
        ----------
        data: str, bytes, int, float
            the data to be stored in the cache

        Returns:
        -------
            a string of uuid key to restore the value with
        """
        _id: str = str(uuid4())
        if isinstance(data, int) or isinstance(data, float):
            data = str(data)
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        self._redis.set(_id, data)
        return _id

    def get(self, key: str, fn: Union[Callable, None] = None) -> Any:
        """
        This function converts data retrieved from the database
        in the desired format based on the function argument

        Parameters:
        ----------
        key: str
            the key of the value to be retrieved
        fn: function
            the callable used to convert th data to the desired
            format

        Returns:
        -------
           the value retrieved
        """
        value: bytes = self._redis.get(key)
        if not fn:
            return value
        return fn(value)

    def get_str(self, key: str) -> str:
        """
        This function converts data retrieved from the database
        as a string

        Parameters:
        ----------
        key: str
            the key of the value to be retrieved

        Returns:
        -------
           the value retrieved
        """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """
        This function converts data retrieved from the database
        as an integer

        Parameters:
        ----------
        key: str
            the key of the value to be retrieved

        Returns:
        -------
           the value retrieved
        """
        return self.get(key, int)
