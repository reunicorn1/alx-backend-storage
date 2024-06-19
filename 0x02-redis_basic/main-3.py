#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

cache = Cache()

cache.store(b"first")
print(cache.get(cache.store.__qualname__))

key = cache.store(b"second")
cache.store(b"third")
cache.get(key)
print(cache.get(cache.store.__qualname__))
print(cache.get(cache.get.__qualname__))
print(cache.get(cache.get_int.__qualname__))
