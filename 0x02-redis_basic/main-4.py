#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

cache = Cache()

print(cache.store.__qualname__)
s1 = cache.store("first")
print(str('first'))
print(s1)
s2 = cache.store(b"foo")
print(str(b"foo"))
print(s2)
s3 = cache.store(1)
print(str(1))
print(s3)

inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))

