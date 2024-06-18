#!/usr/bin/env python3
"""
14. Top students
"""


def top_students(mongo_collection):
    """
    this function that returns all students sorted by average score
    ------------------
    Parameters:
    mongo_collection (pymongo collection object)
    ------------------
    Returns:
        a list of all students sorted by average score
    """
    pipeline = [
            {
                '$addFields': {'id': '$_id'}
            },
            {
                '$unwind': '$topics'
            },
            {
                "$group": {
                    "_id": "$id",
                    'name': {'$first': '$name'},
                    "averageScore": {"$avg": "$topics.score"}
                }
            },
            {
                '$sort': {'averageScore': -1}
            }
        ]
    return mongo_collection.aggregate(pipeline)
