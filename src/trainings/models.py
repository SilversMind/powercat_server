from pydantic import BaseModel
from typing import Dict, Optional

ExerciseResults = Dict[str, bool]
WorkoutResults = Dict[str, ExerciseResults]
TrainingHistory = Optional[Dict[str, WorkoutResults]]


class Exercise(BaseModel):
    exerciseName: str
    set: int
    reps: int
    rpe: float
    weight: float = None

class Training(BaseModel):
    id: int
    exercises: list[Exercise]
    programId: int

class DetailedTraining(Training):
    nbTrainings: int

class TrainingResult(BaseModel):
    name: str
    validatedSets: WorkoutResults
