from src.schemas.song import Song as SongItem
from src.db.base import Song, Artist, song_artist

class SongRepository:

    def __init__(self, db):
        self.db = db

    def add_songs(self, songs: list[SongItem]):
        raise NotImplementedError
    
    def get_all_songs(self) -> list[SongItem]:
        raise NotImplementedError
    
    def update_song(self, id: str, song: Song):
        raise NotImplementedError
    
    def remove_song(self, id: str):
        raise NotImplementedError
