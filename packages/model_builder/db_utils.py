import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def get_card_candidates(name, set_number, mongo_uri=os.getenv('MONGO_CONNECTION_STRING'), db_name="RemodeledTestDB", collection_name="Cards"):
    # Get the collection we will be querying
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Build mongoDB query
    query = {}
    if name:
        query['cardInfo.name'] = { "$regex": name, "$options": "i" }
    if set_number:
        query['set_number'] = set_number

    return list(collection.find(query))
