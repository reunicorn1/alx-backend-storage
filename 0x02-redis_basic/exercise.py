#!/usr/bin/env python3
"""
Redis basic
"""
import redis
from typing import Union
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
