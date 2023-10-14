from fastapi import APIRouter
from src.database import DB
from src.profile.models import Profile
from pydantic import parse_obj_as

profile_router = APIRouter(prefix="/profile")

@profile_router.get("/", response_model=Profile)
def get_profile():
    filter = {'name': "Lolo"}
    projection = {"_id":0}
    return Profile.model_validate(DB["profile"].find_one(filter, projection))