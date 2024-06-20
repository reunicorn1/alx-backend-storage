#!/usr/bin/env python3
""" Main file """
import time
import redis

get_page = __import__('web').get_page
cache = redis.Redis(host='127.0.0.1', port=6379)
cache.flushdb()

urls = ['http://google.com', 'http://slowwly.robertomurray.co.uk']
for url in urls:
    start_time = time.time()
    get_page(url)
    end_time = time.time()
    print(end_time - start_time)


    start_time = time.time()
    get_page(url)
    end_time = time.time()
    print(end_time - start_time)

    start_time = time.time()
    get_page(url)
    end_time = time.time()
    print(end_time - start_time)

    print('the count of ', url, cache.get('count:{}'.format(url)))
