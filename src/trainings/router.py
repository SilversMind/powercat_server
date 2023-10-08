from fastapi import APIRouter
from src.trainings.utils import get_current_training_id
from src.database import DB
from src.trainings.models import Training

trainings_router = APIRouter(prefix="/training")

@trainings_router.get("/")
def get_current_training() -> Training:
    current_training_id = get_current_training_id()
    return DB["training"].find_one({"id": current_training_id},{"_id": 0})

@trainings_router.get("/finish")
def update_training_id() -> None:
    filter = {'last_session': {'$exists': True}}
    update = {'$inc': {'last_session': 1}}
    DB["training"].update_one(filter,  update)