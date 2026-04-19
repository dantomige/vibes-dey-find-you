"""
Two-tower model.
Encoding of user profile + user query. Encoding of song metadata + audio feature (stored in long term after training to find this). Cosine similarity and return top k songs

Cross attention model.
Feed everything into a transformer : [query tokens] + [user features] + [song metadata] + [audio features]
Allows for more complex interaction.


* Make sure to use the same encoder when it comes to vectorizing readable text (queries, titles, genres)

"""

import torch
from torch import nn
import torch.nn.functional as F


class QueryTowerModel(nn.Module):
    def __init__(self, input_dim, embedding_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, embedding_dim),
        )

    def forward(self, x):
        return F.normalize(self.net(x), dim=-1)


class SongTowerModel(nn.Module):
    def __init__(self, input_dim, embedding_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, embedding_dim),
        )

    def forward(self, x):
        return F.normalize(self.net(x), dim=-1)


class TwoTowerModel(nn.Module):
    def __init__(self, query_input_dim, song_input_dim, embedding_dim):
        super().__init__()
        self.query_tower = QueryTowerModel(
            input_dim=query_input_dim, embedding_dim=embedding_dim
        )
        self.song_tower = SongTowerModel(
            input_dim=song_input_dim, embedding_dim=embedding_dim
        )

    def forward(self, query_x: torch.Tensor, songs_x: torch.Tensor):
        q = self.query_tower(query_x)
        s = self.song_tower(songs_x)

        scores = torch.matmul(s, q.T)
        return scores
