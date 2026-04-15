from pydantic import BaseModel
from typing import Optional


class Artist(BaseModel):
    name: str
    recco_beats_id: Optional[str] = None
    music_brainz_id: Optional[str] = None
    # isni: str  ADD BACK LATER
