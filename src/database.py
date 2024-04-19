from pymongo import MongoClient
from pymongo.server_api import ServerApi
from src.settings import DB_URI, DB_NAME

# Init MongoDB connection
client = MongoClient(DB_URI, server_api=ServerApi('1'))
DB = client[DB_NAME]