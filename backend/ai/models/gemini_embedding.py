from langchain_google_genai import GoogleGenerativeAIEmbeddings
from ai.base.base_embedding import BaseEmbeddingModel

class GeminiEmbeddingModel(BaseEmbeddingModel):
    def __init__(self):
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    def embed_query(self, text: str):
        return self.embedding_model.embed_query(text)

    def embed_documents(self, texts):
        return self.embedding_model.embed_documents(texts)