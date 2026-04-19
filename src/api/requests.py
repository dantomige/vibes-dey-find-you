from pydantic import BaseModel

class RecommendRequest(BaseModel):
    query: str
    num_songs: int
