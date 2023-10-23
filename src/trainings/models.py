from pydantic import BaseModel

class Exercise(BaseModel):
    exerciseName: str
    set: int
    reps: int
    rpe: float
    weight: int = None

class Training(BaseModel):
    id: int
    exercises: list[Exercise]
    programId: int

class ProfileName(BaseModel):
    name: str
