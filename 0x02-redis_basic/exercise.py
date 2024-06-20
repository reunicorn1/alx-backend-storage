#!/usr/bin/env python3
"""
Redis basic
"""
from functools import wraps
import redis
from typing import Union, Callable, Any, Tuple, Dict
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
    This is a decorator function that stores te history of inputs
    and ouput for a particular function

    Parameters:
    ----------
    method: Callable

    Returns
    -------
        The wrapper function
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        Returns the method's output after storing its inputs and
        output.
        """
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    """
    Displays the call history of a Cache class' method.
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


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
