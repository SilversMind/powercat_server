from pydantic import BaseModel

class Exercise(BaseModel):
    type: str
    set: int
    reps: int
    rpe: float
    weight: int = None

class Training(BaseModel):
    id: int
    exercises: list[Exercise]