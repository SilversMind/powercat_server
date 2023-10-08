from fastapi import APIRouter
from src.database import DB

profile_router = APIRouter(prefix="/profile")

@profile_router.get("/")
def get_profile():
    filter = {'name': "Lolo"}
    projection = {"_id":0}
    return DB["profile"].find_one(filter, projection)