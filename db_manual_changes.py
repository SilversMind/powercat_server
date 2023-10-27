from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pathlib import Path
from pymongo.collection import Collection
import json
from src.settings import DB_URI

def import_data(filename: str, collection: Collection) -> None:
     with open(Path(__file__).parent / filename) as data_fin:
        collection.delete_many({})
        data = json.load(data_fin)
        for elem in data:
            collection.insert_one(elem)
        # collection.insert_one({"last_session": 1})
        for res in list(collection.find()):
            print(res)

def reset_last_session_index(collection: Collection) -> None:
    filter = {"last_session": {"$exists": True}}
    update = {'$set': {'last_session': 1}}
    collection.update_one(filter, update)
    res = collection.find()

# Create a new client and connect to the server
client = MongoClient(DB_URI, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    database_names = client.list_database_names()
    db = client["powercat"]
    collection = db['profile']
    # reset_last_session_index(collection)
    # import_data("profiles.json", collection)
    filter = {'name': "Lolo"}
    print(collection.find_one(filter, {"current_training_results": 1, "_id": 0}))


except Exception as e:
    print(e)

