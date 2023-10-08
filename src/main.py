from dataclasses import dataclass
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.trainings.router import trainings_router
from src.profile.router import profile_router
from src.calculator.router import calculator_router

# Init API Server
app = FastAPI()
app.include_router(trainings_router)
app.include_router(profile_router)
app.include_router(calculator_router)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"])

@dataclass
class Profile:
    name: str
    PR: dict[str: int]


    




