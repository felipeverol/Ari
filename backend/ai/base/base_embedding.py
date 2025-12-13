from abc import ABC, abstractmethod
from typing import List

class BaseEmbeddingModel(ABC):
    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Generate embedding vector for the given text."""
        pass
    
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embedding vectors for a list of documents."""
        pass