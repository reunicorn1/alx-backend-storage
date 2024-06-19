#!/usr/bin/env python3
"""
Redis basic
"""
import redis
from typing import Union, Callable, Any
from uuid import uuid4


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
        self._redis.flushdb()

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

    def get(self, key: str, fn: Callable) -> Any:
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
        self.get(key, str)

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
        self.get(key, int)





