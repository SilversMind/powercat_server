from pydantic import BaseModel

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

class ProfileName(BaseModel):
    name: str
