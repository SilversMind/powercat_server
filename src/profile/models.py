from typing import Optional
from pydantic import BaseModel
from src.trainings.models import TrainingHistory
class Profile(BaseModel):
    name: str
    PR: dict[str, float]
    current_program: int
    current_training: int
    training_history: Optional[TrainingHistory]
    is_active: bool
    # avatar_path: Optional[str] = None