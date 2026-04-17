import pandas as pd
from src.db.tables.ml import AudioFeaturesModel
from src.schemas.audio_features import AudioFeatures


class AudioFeaturesRepository:

    def __init__(self, db):
        self.db = db

    def add_audio_features(
        self, song_id: str, features: AudioFeatures
    ) -> AudioFeaturesModel:
        raise NotImplementedError

    def get_audio_features(self, song_id: str) -> AudioFeaturesModel | None:
        raise NotImplementedError

    def update_audio_features(
        self, song_id: str, features: AudioFeatures
    ) -> AudioFeaturesModel:
        """Updates the audio features for the given song ID. If no audio features exist for the song ID, raises an exception."""

        raise NotImplementedError

    def remove_audio_features(self, song_id: str) -> bool:
        raise NotImplementedError

    def to_dataframe(self) -> pd.DataFrame:
        raise NotImplementedError
