from fastapi import APIRouter
from src.database import DB
from src.trainings.models import Training, ProfileName
from src.trainings.utils import compute_pr_by_repetition_number
from src.profile.router import get_profile

trainings_router = APIRouter(prefix="/training")

@trainings_router.get("/{training_id}")
def get_current_training(training_id: int) -> Training:
    training = Training.model_validate(DB["training"].find_one({"id": training_id},{"_id": 0}))
    user_pr = get_profile("Lolo").PR
    for exercise in training.exercises:
        exercise.weight = compute_pr_by_repetition_number(user_pr[exercise.exerciseName], exercise.reps, exercise.rpe)

    return training

@trainings_router.post("/finish")
def update_training_id(item: ProfileName) -> None:
    filter = {'name': item.name}
    update = {'$inc': {'current_training': 1}}
    DB["profile"].update_one(filter, update)