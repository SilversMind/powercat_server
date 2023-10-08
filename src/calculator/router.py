from fastapi import APIRouter
from dataclasses import dataclass
from pydantic import BaseModel
from src.calculator.utils import compute_pr_by_repetition_number

TABLE_SIZE = 12
calculator_router = APIRouter(prefix="/calculator")

@dataclass
class RPEDetails:
    weights: list[int]
    rpe: int

class Item(BaseModel):
    PR: int

@calculator_router.post("/")
def write_PR_by_reps(item: Item):
    rpe_tables = {"rpeTables": []}
    for rpe in range(10, 0, -1):
        weights = [compute_pr_by_repetition_number(item.PR, rep, rpe) for rep in range(0, TABLE_SIZE)]
        rpe_tables["rpeTables"].append(RPEDetails(weights=weights, rpe=rpe))
    return rpe_tables