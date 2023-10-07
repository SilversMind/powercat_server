from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pathlib import Path
from pymongo.collection import Collection
import json
from powercat.settings import DB_URI

def import_data(filename: str, collection: Collection) -> None:
     with open(Path(__file__).parent / filename) as training_fin:
        trainings = json.load(training_fin)
        for elem in trainings["sessions"]:
            collection.insert_one(elem)
        collection.insert_one({"last_session": 0})

# Create a new client and connect to the server
client = MongoClient(DB_URI, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    database_names = client.list_database_names()
    db = client["powercat"]
    collection = db['training']
    filter = {'name': {'$eq': "Lol"}}
    # update = {'$set': {'last_session': 0}}
    # collection.update_one(filter,  update)
    res = collection.find()
    print(list(res))
    


except Exception as e:
    print(e)

