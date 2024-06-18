#!/usr/bin/env python3
"""
8. List all documents in Python
"""


def list_all(mongo_collection):
    """
    list_all:  lists all documents in a collection
    -----------------
    Parameters:
    mongo_collection (Pymongo Collection Object)
    -----------------
    Returns:
    a list of all documents in a collection
    or an empty list
    """
    if not isinstance(mongo_collection, Collection):
        return []
    return list(mongo_collection.find())
