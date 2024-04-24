from fastapi import FastAPI, HTTPException
from enum import Enum
from schema import Band

app = FastAPI()

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
                has_albums:bool = False) -> list[Band]:
    band_list = [Band(**b) for b in BANDS]
    if genre:
        band_list = [
            b for b in band_list if b.genre.lower() == genre.value
        ]
    if has_albums:
        band_list = [b for b in band_list if len(b.albums)>0]
    return band_list

@app.get('/bands/{band_id}')
async def band(band_id: int) -> Band:
    band = next((Band(**b) for b in BANDS if b['id'] == band_id ), None)
    if band is None:
        raise HTTPException(status_code=404, detail = 'Band not found')
    return band

# @app.get('/bands/genre/{genre}')
# async def bands_for_genre(genre:GenreURLChoices) -> list[dict]:
#     return [
#         b for b in BANDS if b['genre'].lower() == genre.value
#     ]


