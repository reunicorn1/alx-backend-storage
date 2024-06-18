#!/usr/bin/env python3
"""
9. Insert a document in Python
"""


def insert_school(mongo_collection, **kwargs):
    """
    insert_school: inserts a new document in a collection based on
    kwargs
    ------------
    Parameters:
    mongo_collection: a Pymongo Collection Object
    kwargs: the attributes dict
    ------------
    Returns:
        the new _id
    """
    return mongo_collection.insert_one(kwargs).inserted_id
