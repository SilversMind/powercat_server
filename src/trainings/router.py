from fastapi import APIRouter
from src.database import DB
from src.trainings.models import (
    TrainingResult,
    Set,
    ValidatedSetResponse,
    Training,
)
from src.profile.models import Profile

from src.program.router import get_program
from src.trainings.utils import compute_pr_by_repetition_number
from src.profile.router import get_profile
from pydantic import TypeAdapter


trainings_router = APIRouter(prefix="/training")

def get_training_history(username: str):
    return DB["trainingHistory"].find_one({"name": username})["training_history"]



@trainings_router.get("")
def get_current_training(username: str):
    user = get_profile(username)

    if not get_training_history(username):
        # Si il n'y a pas de training_history, c'est qu'on a besoin de rajouter
        # la séance en cours
        DB["trainingHistory"].update_one(
            {"name": username},
            {
                "$push": {
                    "training_history": generate_user_training(username).model_dump()
                }
            },
        )

    filters = [
        {"$match": {"name": username}},
        {"$unwind": "$training_history"},
        {"$match": {"training_history.training_position": user.current_training}},
        {"$replaceRoot": {"newRoot": "$training_history"}},
    ]
    training = next(DB["trainingHistory"].aggregate(filters))
    return Training.model_validate(training)


def generate_user_training(username: str) -> Training:
    user = get_profile(username)
    test_training = Training.model_validate(
        DB["training"].find_one(
            {
                "program_id": user.current_program,
                "trainings.training_position": user.current_training,
            },
            {"_id": 0, "trainings.$": 1},
        )["trainings"][0]
    )

    for exercise in test_training.exercises:
        for set in exercise.sets:
            set.weight = compute_pr_by_repetition_number(
                user.PR[exercise.name], set.reps, set.rpe
            )
    return test_training


@trainings_router.post("/finish")
def update_training_id(item: TrainingResult) -> None:
    user = get_profile(item.name)
    program = get_program(user.current_program)
    if user.current_training < program.nb_trainings:
        filter = {"name": item.name}
        update = {
            "$inc": {"current_training": 1},
        }
   
    else:
        filter = {"name": item.name}
        update = {
            "$inc": {"current_program": 1},
            "$set": {"current_training": 1}
        }

    DB["profile"].update_one(filter, update)
    next_training = generate_user_training(item.name)
    DB["trainingHistory"].update_one(
        {"name": item.name}, {"$push": {"training_history": next_training.model_dump()}}
    )

@trainings_router.get("/get_current_training_results")
def get_current_training_results(username: str):
    filter = {"name": username}
    projection = {"current_training_results": 1, "_id": 0}
    if (
        training_result := DB["profile"]
        .find_one(filter, projection)
        .get("current_training_results")
    ):
        return TypeAdapter(WorkoutResults).validate_python(training_result)
    return None


@trainings_router.post("/validate_set")
def validate_set(item: ValidatedSetResponse) -> None:
    updated_set = Set(
        id=item.validated.id,
        reps=item.validated.reps,
        rpe=item.validated.rpe,
        weight=item.validated.weight,
        is_validated=item.isValidated,
    )
    filter = {
        "name": item.name,
        "training_history.id": item.trainingId,
        "training_history.exercises.name": item.exerciseName,
        "training_history.exercises.sets.id": item.validated.id,
    }

    update = {
        "$set": {
            "training_history.$[history].exercises.$[exercise].sets.$[set]": updated_set.model_dump()
        }
    }

    DB["trainingHistory"].update_one(
        filter,
        update,
        array_filters=[
            {"history.id": item.trainingId},
            {"exercise.name": item.exerciseName},
            {"set.id": item.validated.id},
        ],
    )
