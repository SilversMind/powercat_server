from fastapi import APIRouter
from src.program.models import Program
from src.database import DB
from src.profile.router import get_profile
program_router = APIRouter(prefix="/program")

def get_program(program_id: int) -> Program:
    nb_trainings = len(DB['training'].find_one({"program_id":program_id})["trainings"])
    return Program.model_validate({"id": program_id, "nb_trainings": nb_trainings})

@program_router.get("")
def get_current_program(username: str) -> Program:
    user = get_profile(username)
    return get_program(user.current_program)