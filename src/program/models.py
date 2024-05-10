from pydantic import BaseModel
from src.trainings.models import Training
from typing import Optional

class Subblock(BaseModel):
    name: str
    start_training_id: int
    end_training_id: int

class Block(BaseModel):
    id: str
    name: str
    subblocks: list[Subblock]

class Program(BaseModel):
    id: int
    name: str
    category: str
    nb_trainings: int = None
    trainings: list[Training]
    blocks: Optional[list[Block]] = None

class Programs(BaseModel):
    programs : list[Program]

class SelectedProgram(BaseModel):
    username: str
    program_id: int

