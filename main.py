from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from pathlib import Path
from dataclasses import dataclass
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils import compute_pr_by_repetition_number
from powercat.settings import DB_URI

# Init API Server
app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"])

# Init MongoDB connection
client = MongoClient(DB_URI, server_api=ServerApi('1'))
DB = client["powercat"]

class Item(BaseModel):
    PR: int

@dataclass
class RPEDetails:
    weights: list[int]
    rpe: int


TABLE_SIZE = 12

@app.post("/calculator")
def write_PR_by_reps(item: Item):
    rpe_tables = {"rpeTables": []}
    for rpe in range(10, 0, -1):
        weights = [compute_pr_by_repetition_number(item.PR, rep, rpe) for rep in range(0, TABLE_SIZE)]
        rpe_tables["rpeTables"].append(RPEDetails(weights=weights, rpe=rpe))
    return rpe_tables

@app.get("/training")
def get_current_training():
    current_training_id = get_current_training_id()
    return DB["training"].find_one({"id": current_training_id},{"_id": 0})

@app.get("/finish_training")
def update_training_id() -> None:
    filter = {'last_session': {'$exists': True}}
    update = {'$inc': {'last_session': 1}}
    DB["training"].update_one(filter,  update)
    
def get_current_training_id() -> int:
    data = DB["training"].find_one({"last_session": {"$exists": True}})
    return data['last_session']




