from fastapi import FastAPI, HTTPException, Path, Query, Depends
from enum import Enum
from models import GenreURLChoices, BandBase, BandCreate, Band, Album
from typing import Annotated
from contextlib import asynccontextmanager
from db import init_db, get_session
from sqlmodel import Session, select

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

class GenreURLChoices(Enum):
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    HIP_HOP = 'hip-hop'

BANDS = [
    {'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
    {'id': 2, 'name': 'Alpha Twin', 'genre': 'Electronic'},
    {'id': 3, 'name': 'Black Sabbath', 'genre': 'Metal', 'albums':[
        {'title': 'Master of Reality', 'release_date': '1971-07-21'}
    ]},
    {'id': 4, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'},
]



@app.get('/bands')
async def bands(genre: GenreURLChoices | None = None,
                q: Annotated[ str | None , Query(max_length=10)] = None,
                session:Session = Depends(get_session)) -> list[Band]:
    
    band_list = session.exec(select(Band)).all()
    if genre:
        band_list = [
            b for b in band_list if b.genre.value.lower() == genre.value
        ]
    if q:
        band_list=[
            b for b in band_list if q.lower() in b.name.lower()
        ]
    return band_list

@app.get('/bands/{band_id}')
async def band(band_id: Annotated[int, Path(title="The band ID")],
               session:Session = Depends(get_session)) -> Band:
    band = session.get(Band, band_id)
    if band is None:
        raise HTTPException(status_code=404, detail = 'Band not found')
    return band

@app.get('/bands/genre/{genre}')
async def bands_for_genre(genre:GenreURLChoices) -> list[dict]:
    return [
        b for b in BANDS if b['genre'].lower() == genre.value
    ]

@app.post("/bands")
async def create_band(
    band_data: BandCreate,
    session:Session = Depends(get_session)) -> Band:
    band = Band(name=band_data.name, genre = band_data.genre)
    session.add(band)
    
    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(
                title = album.title, release_date= album.release_date, band=band
            )
            session.add(album_obj)
    session.commit()
    session.refresh(band)
    return band



