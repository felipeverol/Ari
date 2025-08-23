import argparse
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

CHROMA_PATH = "RAG/chroma"
PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um assistente que deve responder a pergunta APENAS com base no seguinte contexto: {context}\n"
            "Se o contexto indicar que não há informações sobre o assunto, responda educadamente que não sabe sobre tópico.",
        ),
        ("human", "{query}"),
    ]
)

def query(query_text):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embeddings
    )

    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    model = GoogleGenerativeAI(model="gemini-2.5-flash")
    
    if len(results) == 0 or results[0][1] < 0.5:
        context_text = "Não há informações sobre o assunto"
    else:
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    
    chain = PROMPT_TEMPLATE | model
    response_text = chain.invoke({"context": context_text, "query": query_text})

    return response_text

