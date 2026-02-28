from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

def connect_db():
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return collection

def insert_or_update_pothole(collection, pothole_data, duplicate_distance_m=4.57):
    """
    Insert new pothole or update existing if confidence higher.
    Placeholder for geospatial duplicate logic.
    """
    # TODO: Implement geospatial query and update
    collection.insert_one(pothole_data)
    print("Inserted/Updated pothole:", pothole_data)