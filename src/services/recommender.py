import torch
from torch import nn
from src.db.crud.core import SongRepository
from src.schemas.song import Song
from src.db.crud.vector import VectorDBRepository
from src.ml.embedding import EmbeddingModel


class RecommenderService:
    """Service responsible for recommending songs based on a query."""

    def __init__(
        self,
        model: nn.Module,
        song_repository: SongRepository,
        vector_db_repository: VectorDBRepository,
        embedding_model: EmbeddingModel,
    ):
        self.model = model
        self.song_repository = song_repository
        self.vector_db_repository = vector_db_repository
        self.embedding_model = embedding_model

    def recommend_songs(self, query, k=5, search_k=20) -> list[tuple[Song, float]]:
        # 1. Embed the query
        query_vector = self.embedding_model.embed(query)

        # 2. Search for similar song vectors in the vector DB
        results = self.vector_db_repository.search(query_vector, search_k)

        # 3. Use the model to score the results and return top k songs
        scores: torch.Tensor = self.model.forward(query_vector, results["embeddings"])

        # Combine scores with song IDs and sort
        scored_results = list(zip(results["ids"][0], scores.tolist()[0]))
        scored_results.sort(key=lambda x: x[1], reverse=True)

        # 4. Fetch song details for the top k results
        top_song_ids = [song_id for song_id, _ in scored_results[:k]]
        songs = [
            self.song_repository.get_song(song_id=song_id) for song_id in top_song_ids
        ]
        songs = [
            Song(title=song.title, artists=song.artists)
            for song in songs
            if song is not None
        ]
        song_dict = {song.id: song for song in songs}
        scored_songs = [
            (song_dict[song_id], score)
            for song_id, score in scored_results[:k]
            if song_id in song_dict
        ]
        return scored_songs
