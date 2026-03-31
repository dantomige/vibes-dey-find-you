from pydantic import BaseModel


class Artist(BaseModel):
    id: str
    name: str
    # isni: str  ADD BACK LATER
