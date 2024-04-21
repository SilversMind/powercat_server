from fastapi import APIRouter
from src.program.models import Program, Programs
from src.database import DB
from src.profile.router import get_profile
program_router = APIRouter(prefix="/program")

def get_program(program_id: int) -> Program:
    trainings = DB['training'].find_one({"program_id":program_id})["trainings"]
    return Program.model_validate({"id": program_id, "nb_trainings": len(trainings), "trainings": trainings})

@program_router.get("/list-programs")
def get_programs() -> list[Program]:
    programs = [Program(id=obj["program_id"],
                        name=obj["name"],
                        category=obj["category"],
                        nb_trainings=len(obj["trainings"]), 
                        trainings=obj["trainings"])
                 for obj in list(DB['training'].find())]
    return Programs.model_validate(Programs(programs=programs)).programs

@program_router.get("")
def get_current_program(username: str) -> Program:
    user = get_profile(username)
    return get_program(user.current_program)