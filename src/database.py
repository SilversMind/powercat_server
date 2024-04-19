from pymongo import MongoClient
from pymongo.server_api import ServerApi
from src.settings import DB_URI, DB_NAME
import certifi
# Init MongoDB connection
client = MongoClient(DB_URI, server_api=ServerApi('1'), tlsCAfile=certifi.where())
DB = client[DB_NAME]