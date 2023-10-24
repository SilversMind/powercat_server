from fastapi import APIRouter
from src.database import DB
from src.trainings.models import Training, ProfileName, DetailedTraining
from src.trainings.utils import compute_pr_by_repetition_number
from src.profile.router import get_profile

trainings_router = APIRouter(prefix="/training")

@trainings_router.get("/")
def get_current_training(username: str) -> DetailedTraining:
    user = get_profile(username)
    training = Training.model_validate(DB["training"].find_one({"id": user.current_training},{"_id": 0}))
    nb_trainings = DB['training'].count_documents({"programId":user.current_program})

    for exercise in training.exercises:
        exercise.weight = compute_pr_by_repetition_number(user.PR[exercise.exerciseName], exercise.reps, exercise.rpe)
    
    detailed_training = DetailedTraining.model_validate(training.model_dump() | {"nbTrainings": nb_trainings})
    return detailed_training

@trainings_router.post("/finish")
def update_training_id(item: ProfileName) -> None:
    filter = {'name': item.name}
    update = {'$inc': {'current_training': 1}}
    DB["profile"].update_one(filter, update)