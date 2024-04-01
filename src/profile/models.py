from pydantic import BaseModel, Field, AliasPath
class Profile(BaseModel):
    name: str
    PR: dict[str, float]
    current_program: int
    current_training: int
    is_active: bool = Field(alias=AliasPath("isActive"))
    # avatar_path: Optional[str] = None