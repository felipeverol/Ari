from langchain_google_genai import ChatGoogleGenerativeAI
from utils.ai.base_llm import BaseLLM

class Gemini25Flash(BaseLLM):
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")
    
    def generate(self, prompt: str) -> str:
        return self.llm.invoke(prompt)