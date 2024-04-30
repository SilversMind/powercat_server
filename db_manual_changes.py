from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pathlib import Path
from pymongo.collection import Collection
import json
from src.settings import DB_URI
from src.trainings.models import Training, Set


def set_training(profiles, username: str, training_id: int, program_id: int):
    profiles.update_one(
        {"name": username},
        {
            "$set": {"current_training": training_id, "current_program": program_id},
        },
    )
    print(profiles.find_one({"name": username}))


def reset_app_dbs():
    import_data("traininghistory.json", db["trainingHistory"])
    import_data("testprogram1.json", db["training"])
    reset_last_session_index()


def import_data(filename: str, collection: Collection) -> None:
    with open(Path(__file__).parent / filename) as data_fin:
        collection.delete_many({})
        data = json.load(data_fin)
        for elem in data:
            collection.insert_one(elem)
        # collection.insert_one({"last_session": 1})
        for res in list(collection.find()):
            print()


def reset_last_session_index() -> None:
    collection = db["profile"]
    filter = {"name": "Lolo"}
    update = {"$set": {"current_training": 1}}
    collection.update_one(filter, update)


# Create a new client and connect to the server
client = MongoClient(DB_URI, server_api=ServerApi("1"))
db = client["powercat"]
collection : Collection = db["profile"] 
# import_data(filename="testprogram1.json", collection=collection)
filter = {"name": "Lolo"}
update = {
    "$set": {"current_program": 1}
}
# collection.update_one(filter=filter, update=update)
print(collection.find_one(filter=filter))
# Send a ping to confirm a successful connection
# try:
#     database_names = client.list_database_names()
#     db = client["powercat"]
#     collection = db["trainingHistory"]
#     filters = [
#         {"$match": {"name": "Lolo"}},
#         {"$unwind": "$training_history"},
#         {"$match": {"training_history.training_position": 1}},
#         {"$replaceRoot": {"newRoot": "$training_history"}},
#     ]
#     set_training(db["profile"], "Lolo", program_id=1, training_id=10)

    # training = next(collection.aggregate(filters))
    # print(training)
    # reset_last_session_index()
    # reset_app_dbs()

