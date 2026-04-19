import pandas as pd


class MusicPreprocessor:

    def __init__(self):
        # store learned stats for consistency (train vs inference)
        self.audio_feature_medians = {}

    # -----------------------------
    # AUDIO FEATURES CLEANING
    # -----------------------------
    def clean_audio_features(self, audio_df: pd.DataFrame) -> pd.DataFrame:
        df = audio_df.copy()

        expected_cols = [
            "song_id", "danceability", "energy", "key", "loudness",
            "mode", "speechiness", "acousticness", "instrumentalness",
            "liveness", "valence", "tempo"
        ]

        # Validate schema
        missing = set(expected_cols) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        df = df.drop_duplicates(subset=["song_id"])

        numeric_cols = [col for col in expected_cols if col != "song_id"]

        for col in numeric_cols:
            if df[col].isnull().any():
                median = df[col].median()
                self.audio_feature_medians[col] = median
                df[col] = df[col].fillna(median)

        df["tempo"] = df["tempo"].clip(lower=0)

        return df

    # -----------------------------
    # SONG FEATURES CLEANING
    # -----------------------------
    def clean_song_features(self, song_df: pd.DataFrame) -> pd.DataFrame:
        df = song_df.copy()

        expected_cols = [
            "id", "music_brainz_id", "recco_beats_id",
            "isrc", "title", "duration"
        ]

        # Validate schema
        missing = set(expected_cols) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        df = df.drop_duplicates(subset=["id"])

        df["title"] = df["title"].str.strip()

        df = df[df["duration"].isnull() | (df["duration"] > 0)]

        if df["duration"].isnull().any():
            df["duration"] = df["duration"].fillna(df["duration"].median())

        df["id"] = df["id"].astype(str)
        df["music_brainz_id"] = df["music_brainz_id"].astype(str)
        df["recco_beats_id"] = df["recco_beats_id"].astype(str)

        return df