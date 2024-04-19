from pymongo import MongoClient
from pymongo.server_api import ServerApi
from src.settings import DB_URI, DB_NAME
import certifi
import logging

logging.logging.info(certifi.where())
# Init MongoDB connection
client = MongoClient(DB_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
DB = client[DB_NAME]