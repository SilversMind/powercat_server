from pydantic import BaseModel

class Exercise(BaseModel):
    type: str
    set: int
    reps: int
    rpe: int

class Training(BaseModel):
    id: int
    exercises: list[Exercise]