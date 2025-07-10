"""
Storage Module

Handles logging of resume analysis requests into a MongoDB collection.

Environment Variables:
----------------------
- MONGO_URI : URI connection string for MongoDB (default: "mongodb://mongo:27017")

Collections:
------------
- talentai.logs : Stores log entries of analyzed requests
"""

import os
from pymongo import MongoClient

# MongoDB connection using environment variable or default URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
client = MongoClient(MONGO_URI)

# Database and collection setup
db = client["talentai"]
logs = db["logs"]

def log_request(log: dict):
    """
    Inserts a log entry into the MongoDB collection.

    Args:
        log (dict): A dictionary containing metadata about a resume analysis request.
                    Expected fields include request_id, user_id, timestamp, query, and result.

    Returns:
        None
    """
    logs.insert_one(log)
