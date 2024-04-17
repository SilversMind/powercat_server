from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi
from src.settings import DB_URI, DB_NAME

ca = certifi.where()
# Init MongoDB connection
client = MongoClient(DB_URI, server_api=ServerApi('1'), tlsCAFile=ca)
DB = client[DB_NAME]