import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader

# takes in the cleaned and engineered features, outputs batches for training

class ListeningDataset(Dataset):
    def __init__(self, song_df: pd.DataFrame, audio_df: pd.DataFrame, query_song_pairs: pd.DataFrame):
        self.song_df = song_df
        self.audio_df = audio_df
        self.query_song_pairs = query_song_pairs # (query, song_id, label)

    def __len__(self):
        return len(self.song_df)

    def __getitem__(self, idx):
        return self.song_df.iloc[idx]