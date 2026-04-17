import torch
import chromadb
from chromadb.api import QueryResult

class VectorDBRepository:

    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name="song_vectors")

    def add_vector(self, song_id: str, vector: torch.Tensor) -> None:
        self.collection.add(ids=[song_id], embeddings=vector.tolist())

    def get_vector(self, song_id: str) -> torch.Tensor | None:
        result = self.collection.get(ids=[song_id])
        if result["ids"]:
            return torch.tensor(result["embeddings"][0])
        return None

    def update_vector(self, song_id: str, vector: torch.Tensor) -> None:
        self.collection.update(ids=[song_id], embeddings=vector.tolist())
    
    def remove_vector(self, song_id: str) -> None:
        self.collection.delete(ids=[song_id])

    def search(self, query: str, k: int) -> QueryResult:
        vector = self.encode(query)

        return self.collection.query(
            query_embeddings=[vector],
            n_results=k
        )