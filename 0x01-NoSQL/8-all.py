#!/usr/bin/env python3
"""
8. List all documents in Python
"""
from typing import List
from pymongo.collection import Collection

if __name__ == "__main__":
    def list_all(mongo_collection: Collection) -> List:
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
