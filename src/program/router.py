from fastapi import APIRouter
from src.program.models import Program, Programs, SelectedProgram
from src.trainings.models import Training
from src.database import DB
from src.trainings.utils import generate_weight
from src.profile.router import get_profile
program_router = APIRouter(prefix="/program")

def get_program(program_id: int) -> Program:
    program_data = DB['training'].find_one({"program_id":program_id})
    return Program.model_validate({"id": program_id,
                                    "nb_trainings": len(program_data["trainings"]),
                                    "trainings": program_data["trainings"],
                                    "name":program_data["name"],
                                    "category":program_data["category"]})

@program_router.get("/list-programs")
def get_programs(username: str) -> list[Program]:
    programs = []
    user_profile = get_profile(username)
    for program in list(DB['training'].find()):
        trainings = [generate_weight(user_profile, Training(**training)) for training in program["trainings"] ]
        programs.append(Program(id=program["program_id"],
                        name=program["name"],
                        category=program["category"],
                        nb_trainings=len(program["trainings"]), 
                        trainings=trainings))
    
    return Programs.model_validate(Programs(programs=programs)).programs

@program_router.post("/select")
def update_programs(selected_program: SelectedProgram) -> None:
    filter = {"name": selected_program.username}
    update = {
        "$set": {"current_program": selected_program.program_id}
    }
    DB["profile"].update_one(filter=filter, update=update)

@program_router.get("")
def get_current_program(username: str) -> Program:
    user = get_profile(username)
    return get_program(user.current_program)