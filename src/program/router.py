from fastapi import APIRouter
from src.program.models import Program
from src.database import DB
program_router = APIRouter(prefix="/program")

@program_router.get("/{program_id}")
def get_program(program_id: int) -> Program:
    nb_trainings = DB['training'].count_documents({"programId":program_id})
    return Program.model_validate({"id": program_id, "nb_trainings": nb_trainings})