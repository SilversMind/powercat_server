from pydantic import BaseModel

class Program(BaseModel):
    id: int
    nb_trainings: int = None