from typing import Union
import json
from pathlib import Path
from dataclasses import dataclass
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils import compute_pr_by_repetition_number
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
def get_training():
    with open(Path(__file__).parent / "trainings.json") as training_fin:
        trainings = json.load(training_fin)
        return trainings["TR1"]


