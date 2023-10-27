from typing import Optional
from pydantic import BaseModel
from src.trainings.models import TrainingHistory, WorkoutResults
class Profile(BaseModel):
    name: str
    PR: dict[str, float]
    current_program: int
    current_training: int
    current_training_results: Optional[WorkoutResults] = None
    training_history: Optional[TrainingHistory]
    is_active: bool
    # avatar_path: Optional[str] = None