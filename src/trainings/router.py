from fastapi import APIRouter
from src.trainings.utils import get_current_training_id
from src.database import DB
from src.trainings.models import Training
from src.calculator.utils import compute_pr_by_repetition_number
from src.profile.router import get_profile

trainings_router = APIRouter(prefix="/training")

@trainings_router.get("/")
def get_current_training() -> Training:
    current_training_id = get_current_training_id()
    training = Training.model_validate(DB["training"].find_one({"id": current_training_id},{"_id": 0}))
    user_pr = get_profile().PR
    for exercise in training.exercises:
        exercise.weight = compute_pr_by_repetition_number(user_pr[exercise.type], exercise.reps, exercise.rpe)

    return training

@trainings_router.get("/finish")
def update_training_id() -> None:
    filter = {'last_session': {'$exists': True}}
    update = {'$inc': {'last_session': 1}}
    DB["training"].update_one(filter,  update)