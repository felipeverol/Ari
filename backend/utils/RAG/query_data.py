import argparse
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# Caminho para o Chroma e o prompt template
CHROMA_PATH = "backend/utils/RAG/chroma"
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
    """
    Consulta a base vetorial (Chroma) e retorna uma resposta usando RAG.

    Etapas:
    - Gera embeddings para a query.
    - Busca os k=3 documentos mais relevantes no Chroma.
    - Avalia a relevância dos resultados (score >= 0.5).
    - Monta o contexto a partir dos documentos encontrados.
    - Executa o modelo Gemini com o contexto e a query.

    Args:
        query_text (str): Texto da consulta do usuário.

    Returns:
        str: Resposta gerada pelo modelo baseada no contexto.
    """
    # Inicializa embeddings e conecta ao banco
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embeddings
    )

    # Busca os 3 documentos mais relevantes
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    model = GoogleGenerativeAI(model="gemini-2.5-flash")
    
    # Caso não encontre resultados relevantes
    if len(results) == 0 or results[0][1] < 0.5:
        context_text = "Não há informações sobre o assunto"
    else:
        # Junta os trechos de documentos como contexto
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    
    # Executa o prompt no modelo
    chain = PROMPT_TEMPLATE | model
    response_text = chain.invoke({"context": context_text, "query": query_text})

    return response_text

