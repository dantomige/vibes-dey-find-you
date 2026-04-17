import torch
from sentence_transformers import SentenceTransformer

class Embedding:

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> torch.Tensor:
        return self.model.encode(text, convert_to_tensor=True)