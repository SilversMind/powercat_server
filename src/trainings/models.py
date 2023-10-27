from pydantic import BaseModel
from typing import Dict, Optional

ExerciseResults = Dict[str, bool] # set n: bool
WorkoutResults = Optional[Dict[str, ExerciseResults]] # exercice n : ExerciceResults
TrainingHistory = Optional[Dict[str, WorkoutResults]] # Seance n : WorkoutResults

class SetContent(BaseModel):
    id: int
    reps: int
    rpe: float
    weight: float = None
    exerciseName: str

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

class ValidatedSetResponse(BaseModel):
    name: str
    validated: SetContent
    isValidated: bool
