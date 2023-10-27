from fastapi import APIRouter
from src.database import DB
from src.trainings.models import Training, TrainingResult, DetailedTraining, ValidatedSetResponse, WorkoutResults
from src.trainings.utils import compute_pr_by_repetition_number
from src.profile.router import get_profile
from pydantic import TypeAdapter


trainings_router = APIRouter(prefix="/training")

@trainings_router.get("")
def get_current_training(username: str) -> DetailedTraining:
    user = get_profile(username)
    training = Training.model_validate(DB["training"].find_one({"id": user.current_training},{"_id": 0}))
    nb_trainings = DB['training'].count_documents({"programId":user.current_program})

    for exercise in training.exercises:
        exercise.weight = compute_pr_by_repetition_number(user.PR[exercise.exerciseName], exercise.reps, exercise.rpe)
    
    detailed_training = DetailedTraining.model_validate(training.model_dump() | {"nbTrainings": nb_trainings})
    return detailed_training

@trainings_router.post("/finish")
def update_training_id(item: TrainingResult) -> None:
    user = get_profile(item.name)
    
    
    training_history = (user.training_history or {}) | {f"Seance {user.current_training}": user.current_training_results}
    filter = {'name': item.name}
    update = {'$inc': {'current_training': 1},
               '$set': {'training_history': training_history, 'current_training_results': None}}
    
    DB["profile"].update_one(filter, update)
    print(DB["profile"].find_one(filter))

@trainings_router.get("/get_current_training_results")
def get_current_training_results(username: str):
    filter = {'name': username}
    projection = {"current_training_results": 1, "_id": 0}
    if training_result := DB["profile"].find_one(filter, projection).get('current_training_results'):
        return TypeAdapter(WorkoutResults).validate_python(training_result)
    return None


@trainings_router.post("/validate_set")
def validate_set(item: ValidatedSetResponse) -> None:
    user = get_profile(item.name)
    current_training_results = user.current_training_results

    if not current_training_results:
        current_training_results = {}

    validated_exercises = current_training_results.get(item.validated.exerciseName, {})
    new_exercise_results = validated_exercises | {str(item.validated.id): item.isValidated}
    set_result: WorkoutResults = {item.validated.exerciseName: new_exercise_results}
    
    current_training_results = current_training_results | set_result
    TypeAdapter(WorkoutResults).validate_python(current_training_results)

    filter = {'name': item.name}
    update = {'$set': {'current_training_results': current_training_results}}
    DB["profile"].update_one(filter, update)