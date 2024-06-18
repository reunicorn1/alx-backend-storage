#!/usr/bin/env python3
"""
12. Log stats
"""
from pymongo import MongoClient

def print_log(collection):
    """
    This function prints the count documents of a collection
    of logs nginx
    ----------------
    Parameters:
    mongo_collection (a pymongo collection object)
    """
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print(collection.count_documents({}), 'logs')
    print('Methods:')
    for method in methods:
        number = collection.count_documents({'method': method})
        print('\tmethod {}: {}'.format(method, number))
    one_line = collection.count_documents({'method': 'GET', 'path': '/status'})
    print('{} status check'.format(one_line))

def main():
    """
    main entry point
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    print_log(collection)


if __name__ == "__main__":
    main()

