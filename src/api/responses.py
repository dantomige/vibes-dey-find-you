from typing import Optional
from pydantic import BaseModel

class RecommendResponse(BaseModel):
    query: str
    songs: list["SongResponse"]

class SongResponse(BaseModel):
    id : str
    title: str
    artists: list[str]

    duration: Optional[int] = None
    
    audio_url: Optional[str] = None
    preview_url: Optional[str] = None
    spotify_url: Optional[str] = None

    score: Optional[float] = None
