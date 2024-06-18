#!/usr/bin/env python3
"""
10. Change school topics
"""


def update_topics(mongo_collection, name, topics):
    """
    update_topics: changes all topics of a school document based
    on the name
    -----------
    Parameters:
    mongo_collection (pymongo collection object)
    name (string)
    topics (List[string])
    -----------
    Returns:
        None
    """
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
