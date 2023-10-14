from pydantic import BaseModel

class Profile(BaseModel):
    name: str
    PR: dict[str, int]