from pydantic import BaseModel
from typing import Dict, Optional


class TrainingResult(BaseModel):
    name: str

class Set(BaseModel):
    id: str
    reps: int
    rpe: float
    weight: Optional[float or None] = None
    is_validated: Optional[bool or None] = None

class Exercise(BaseModel):
    name: str
    sets: list[Set]

class Training(BaseModel):
    id: str
    training_position: int # Séance numéro x
    exercises: list[Exercise]

class Program(BaseModel):
    id: str
    trainings: list[Training]

class ValidatedSetResponse(BaseModel):
    name: str
    validated: Set
    isValidated: bool
    exerciseName: str
    trainingId: str