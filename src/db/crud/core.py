import pandas as pd
from src.schemas.song import Song
from src.db.tables.core import SongModel, ArtistModel, song_artists_table


class SongRepository:

    def __init__(self, db):
        self.db = db

    def get_song_ids_by_external_id(
        self,
        isrc: str | None = None,
        music_brainz_id: str | None = None,
        recco_beats_id: str | None = None,
    ) -> str | None:
        """
        Fetches the song ID corresponding to the given external
        IDs (music_brainz_id, recco_beats_id, isrc).
        Returns the song ID if a match is found, or None if no match is found.
        """
        raise NotImplementedError

    def add_songs(self, songs: list[Song]) -> list[str]:
        raise NotImplementedError

    def get_song(self, song_id: str) -> SongModel | None:
        raise NotImplementedError

    def get_all_songs(self) -> list[SongModel]:
        raise NotImplementedError

    def update_song(self, song_id: str, song: Song):
        raise NotImplementedError

    def remove_song(self, song_id: str):
        raise NotImplementedError

    def to_dataframe(self) -> pd.DataFrame:
        raise NotImplementedError
