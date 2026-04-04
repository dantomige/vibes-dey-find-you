from pydantic import BaseModel


class Artist(BaseModel):
    arid: str
    name: str
    # isni: str  ADD BACK LATER
