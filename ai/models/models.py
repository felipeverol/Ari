from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_cohere.rerank import CohereRerank
from dotenv import load_dotenv

load_dotenv()

gemini_embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
gemini_25_flash = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
gemini_25_flash_lite = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

reranker = CohereRerank(model="rerank-v4.0-fast")