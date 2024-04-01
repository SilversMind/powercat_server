from fastapi import APIRouter, HTTPException
from src.database import DB
from src.profile.models import Profile
from typing import List

profile_router = APIRouter(prefix="/profile")

@profile_router.get("/", response_model=Profile)
def get_profile(username: str):
    filter = {'name': username}
    projection = {"_id":0}
    profile = DB["profile"].find_one(filter, projection)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return Profile.model_validate(profile)

@profile_router.get("/active-users", response_model=list[str])
def get_active_users():
    filter = {'isActive': True}
    projection = {"_id":0}
    return [Profile(**profile).name for profile in DB["profile"].find(filter, projection)]