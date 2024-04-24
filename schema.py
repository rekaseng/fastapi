from enum import Enum
from pydantic import BaseModel
from datetime import date

class GenreURLChoices(Enum):
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    HIP_HOP = 'hip-hop'

class Album(BaseModel):
    title: str
    release_date: date

class Band(BaseModel):
    id:int
    name: str
    genre: str
    albums: list[Album] = None
