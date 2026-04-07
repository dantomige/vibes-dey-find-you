from src.schemas.song import Song
from src.db.base import SongModel, ArtistModel, song_artists_table

class SongRepository:

    def __init__(self, db):
        self.db = db

    def add_songs(self, songs: list[Song]):
        raise NotImplementedError
    
    def get_song(self, mbid: str):
        raise NotImplementedError
    
    def get_all_songs(self) -> list[Song]:
        raise NotImplementedError
    
    def update_song(self, mbid: str, song: Song):
        raise NotImplementedError
    
    def remove_song(self, mbid: str):
        raise NotImplementedError

    def to_dataframe(self):
        raise NotImplementedError