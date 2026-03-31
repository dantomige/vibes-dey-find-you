from pydantic import BaseModel

class Artist(BaseModel):
    isni: str
    name: str