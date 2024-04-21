from pydantic import BaseModel
from src.trainings.models import Training

class Program(BaseModel):
    id: int
    name: str
    category: str
    nb_trainings: int = None
    trainings: list[Training]

class Programs(BaseModel):
    programs : list[Program]