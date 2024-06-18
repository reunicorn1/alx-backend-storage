#!/usr/bin/env python3
"""
12. Log stats
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print(collection.count_documents({}), ' logs')
    print('Methods:')
    for method in methods:
        number = collection.count_documents({'method': method})
        print('\tmethod {}: {}'.format(method, number))
    one_line = collection.count_documents({'method': 'GET', 'path': '/status'})
    print('{} status check'.format(one_line))
