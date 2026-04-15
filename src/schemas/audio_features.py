from pydantic import BaseModel

class AudioFeatures(BaseModel):
    acousticness: float
    danceability: float
    energy: float
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: int
    speechiness: float
    tempo: float
    valence: float