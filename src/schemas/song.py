import hashlib
from typing import Optional
from pydantic import BaseModel
from src.schemas.date import Date
from src.schemas.artist import Artist
from src.schemas.audio_features import AudioFeatures


class Song(BaseModel):
    title: str
    artists: list[Artist]
    rid: Optional[str] = None
    recco_beats_id: Optional[str] = None
    isrc: Optional[str] = None
    release_date: Optional[Date] = None
    genre: Optional[list[str]] = None
    duration: Optional[int] = None  # duration in milliseconds
    album: Optional[int] = None
    language: Optional[str] = None
    audio_url: Optional[str] = None
    audio_features: Optional[AudioFeatures] = None

    @property
    def mbid(self) -> str:
        normalized = f"{self.title.lower()}|{'|'.join(sorted(a.arid for a in self.artists))}|{self.duration or ''}"
        return hashlib.sha256(normalized.encode()).hexdigest()
