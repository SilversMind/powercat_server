from pydantic import BaseModel

class Profile(BaseModel):
    name: str
    PR: dict[str, float]
    current_program: int
    current_training: int