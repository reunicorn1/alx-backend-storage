#!/usr/bin/env python3
"""
11. Where can I learn Python?
"""


def schools_by_topic(mongo_collection, topic):
    """
    schools_by_topic: returns the list of school having a specific
    topic
    ----------------
    Parameters:
    mongo_collection (pymongo collection object):
        pymongo collection object
    topic (string):
        topic searched
    ---------------
    Returns:
        the list of school having a specific topic
    """
    return list(mongo_collection.find({'topics': topic}))
