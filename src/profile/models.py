from pydantic import BaseModel

class Profile(BaseModel):
    name: str
    PR: dict[str, int]
    current_program: int
    current_training: int
    is_training_inprogress: bool