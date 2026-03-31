from artist import Artist
from pydantic import BaseModel

class Song(BaseModel):
    id: int
    title: str
    artists: list[Artist]
    release_date: str
    genre: str
    duration: int # duration in milliseconds
    language: str

# class Song(BaseModel):
#     id: int
#     title: str
#     artists: list[Artist]
#     album: str
#     release_date: str
#     genre: str
#     duration: float
#     language: str
#     audio_url: str