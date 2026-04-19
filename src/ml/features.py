import pandas as pd
from pathlib import Path

class FeatureEngineer:
        
    def prepare_metadata_features(self, df: pd.DataFrame, encoder) -> pd.DataFrame:
        df = df.copy()

        expected_cols = ["id", "title", "duration"]
        self._validate_columns(df, expected_cols)

        embeddings = df["title"].apply(lambda x: encoder.embed(x))
        embedding_dim = len(embeddings.iloc[0])
        embedding_df = pd.DataFrame(embeddings.tolist(), columns=[f"title_emb_{i}" for i in range(embedding_dim)])

        df = pd.concat([df[["id", "title_length", "duration_minutes"]], embedding_df], axis=1)

        # Example features
        df["title_length"] = df["title"].apply(len)
        df["duration_minutes"] = df["duration"] / 60

        return df

    def prepare_audio_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        expected_cols = [
            "song_id", "danceability", "energy", "loudness",
            "speechiness", "acousticness", "instrumentalness",
            "liveness", "valence", "tempo"
        ]
        self._validate_columns(df, expected_cols)

        # Example engineered features
        df["energy_danceability"] = df["energy"] * df["danceability"]
        df["is_high_energy"] = (df["energy"] > 0.7).astype(int)
        df["tempo_scaled"] = df["tempo"] / 200  # simple normalization

        return df
    
    def save_features(self, df: pd.DataFrame, path: Path):
        raise NotImplementedError

    def _validate_columns(self, df, expected_cols):
        missing = set(expected_cols) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")
# feature ideas: vector embedding of the title, categorical variable of type of afrobeats