# Ari

### AI-powered study assistant for educational environments

Ari is an AI-powered educational platform that allows students to interact with the learning materials used in their classes through a context-aware assistant.

Instead of relying solely on a language model's general knowledge, Ari grounds its responses in the content provided by teachers and schools. Documents are processed, indexed, retrieved through a hybrid search pipeline, reranked, and provided to a Gemini-based assistant through an agentic workflow.

**The goal:** turn a class's own learning material into an interactive and contextual study experience.

---

## ✨ Overview

Ari was designed around a simple product problem:

> **How can students interact naturally with the material their teachers already use?**

Teachers make learning materials available to their classes, and students can then use Ari to ask questions about that content.

The platform combines:

- 📚 Class-specific learning materials
- 🤖 AI-powered conversational assistance
- 🔎 Hybrid semantic and lexical retrieval
- 🧠 Agentic orchestration with LangGraph
- 🖼️ Multimodal document understanding
- 🔐 Authentication and role-based authorization
- ⚡ Streaming responses
- 💾 Persistent conversational state

The result is an AI assistant that is aware of **what the student is studying and which class the student belongs to**.

---

## 🧠 AI Pipeline

Ari's question-answering system is implemented as a stateful **LangGraph workflow**.

The LLM can decide whether a question requires information retrieval. When retrieval is necessary, Ari executes a dedicated retrieval tool before generating the final response.

The workflow consists of:

1. **Query / response generation** — Gemini interprets the student's question and determines whether retrieval is necessary.
2. **Hybrid retrieval** — semantic vector search and PostgreSQL full-text search run over the student's class material.
3. **RRF fusion** — results from both retrieval strategies are combined using Reciprocal Rank Fusion.
4. **Reranking** — candidate documents are reranked using Cohere Rerank.
5. **Context construction** — the most relevant textual and visual content is assembled into the model context.
6. **Answer generation** — Gemini produces the final response using the retrieved material.

This separates retrieval into distinct stages, allowing the system to prioritize **recall during search** and **precision during reranking**.

---

## 🔎 Hybrid Retrieval

Ari combines two complementary retrieval strategies.

### Dense retrieval

Document chunks are embedded using Google's embedding models and stored in Supabase/PostgreSQL for vector similarity search.

This allows the system to retrieve conceptually related content even when the student's wording differs from the original material.

### Sparse retrieval

The same query is also processed using PostgreSQL full-text search.

This is particularly useful for:

- Exact terminology
- Names
- Technical concepts
- Keywords
- Expressions that should match literally

### Reciprocal Rank Fusion

The results from dense and sparse retrieval are merged using **Reciprocal Rank Fusion (RRF)**.

RRF combines the rankings themselves rather than relying on the raw scores produced by the two retrieval systems, whose scoring mechanisms are fundamentally different.

The resulting candidate set is then passed to the reranking stage.

---

## 🎯 Reranking

Retrieval is intentionally optimized for finding a broad candidate set.

Ari subsequently uses **Cohere Rerank** to perform a more focused relevance assessment over the retrieved documents.

The final context is constructed from the highest-ranked results before being sent to Gemini.

This creates a multi-stage retrieval pipeline:

> **Retrieve broadly → fuse results → rerank precisely → generate**

---

## 🖼️ Multimodal Documents

Educational material is not exclusively textual.

PDFs may contain diagrams, figures, charts, screenshots, and other visual information that can be important to understanding a subject.

During ingestion, Ari extracts both:

- Text
- Relevant embedded images

Text is chunked and embedded, while extracted images remain associated with their source material and page metadata.

When visual content is retrieved, Ari can provide it to Gemini alongside the textual context, enabling the assistant to reason over both modalities.

---

## 📚 Document Ingestion

When a learning material is uploaded, it goes through a processing pipeline:

**PDF → extraction → chunking → embeddings → storage → retrieval**

PDF processing is handled with **PyMuPDF**.

Text is split using `RecursiveCharacterTextSplitter` with:

- **Chunk size:** 800 characters
- **Overlap:** 150 characters

Chunks retain metadata such as their originating material, class, and page.

The processed content is persisted in Supabase, allowing it to become part of the class's searchable knowledge base.

---

## 💬 Conversational Context

Ari supports persistent conversations rather than treating every question as an isolated request.

Chat state is associated with the student's context and persisted through a PostgreSQL-backed LangGraph checkpointer.

The system also controls the amount of conversational history sent to the model, maintaining relevant context without continuously growing the prompt.

Responses are streamed to the client using **Server-Sent Events (SSE)**, allowing users to see the answer as it is generated.

---

## 🔐 Authentication & Authorization

Ari uses **Supabase Auth** for authentication.

The application implements role-based and resource-aware authorization for:

- **Administrators**
- **Teachers**
- **Students**

Access is not determined solely by a user's global role.

For class-specific resources, the backend also verifies the user's relationship with the corresponding class.

This ensures that the AI retrieval layer operates within the same boundaries as the educational application.

---

## 🏗️ Backend Architecture

The backend is implemented with **FastAPI** and follows a layered architecture.

| Layer           | Responsibility                         |
| --------------- | -------------------------------------- |
| `routes/`       | HTTP endpoints and routing             |
| `controllers/`  | Request handling and API orchestration |
| `services/`     | Application and business logic         |
| `models/`       | Request/response and domain schemas    |
| `dependencies/` | Authentication and authorization       |
| `ai/`           | LLM, retrieval and LangGraph logic     |

The AI subsystem is kept separate from the general application layer, making the retrieval and generation workflow independently understandable and maintainable.

---

## 📁 Project Structure

```text
Ari-Server/
│
├── ai/
│   ├── graph/
│   │   ├── builder.py
│   │   └── nodes.py
│   ├── models/
│   ├── prompts/
│   ├── schemas/
│   └── tools/
│       └── retriever.py
│
├── controllers/
├── dependencies/
├── models/
├── routes/
├── services/
│
├── app.py
├── supabase_client.py
└── requirements.txt
```

The repository is organized around the separation between the **product/application layer** and the **AI/retrieval layer**.

---

## 🛠️ Technology Stack

### Backend

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-Data%20Validation-E92063)

### AI

![Gemini](https://img.shields.io/badge/Google%20Gemini-LLM-4285F4?logo=google&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20Workflow-1C3C3C)
![Cohere](https://img.shields.io/badge/Cohere-Reranking-39594D)

### Data & Infrastructure

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-Backend-3FCF8E?logo=supabase&logoColor=white)

### Document Processing

- PyMuPDF
- Pillow
- LangChain text splitters

---

## ⚙️ Running Locally

### Requirements

- Python 3.10+
- A Supabase project
- Google Gemini API access
- Cohere API access

### Installation

```bash
git clone https://github.com/felipeverol/Ari-Server.git
cd Ari-Server

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### Environment variables

Create a `.env` file with the required credentials:

```env
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE=...
SUPABASE_DB_URI=...
GOOGLE_API_KEY=...
COHERE_API_KEY=...
```

The corresponding database schema and retrieval functions must also be configured in Supabase.

### Start the API

```bash
uvicorn app:app --reload
```

Once running, the API documentation is available through FastAPI's interactive documentation.

---

## 🔬 Engineering Decisions

### Why RAG?

Ari needs to answer questions about **specific educational materials**. RAG allows the system to ground its responses in the content provided by the teacher instead of depending exclusively on the model's parametric knowledge.

### Why hybrid retrieval?

Semantic similarity and lexical matching solve different retrieval problems. Combining them improves coverage across both conceptual and exact-match queries.

### Why RRF?

Dense and sparse retrieval produce different scoring systems. RRF combines their rankings without requiring score calibration between the two approaches.

### Why reranking?

Initial retrieval prioritizes recall. Reranking provides a second relevance stage that improves the quality of the context before expensive LLM generation.

### Why LangGraph?

The AI pipeline has explicit state, conditional execution, tool invocation, and persistent conversational state. LangGraph provides a natural representation for this workflow.

### Why class-scoped retrieval?

Ari is an educational product, not a general-purpose chatbot. The assistant should reason over the knowledge available to the student's class rather than unrelated materials.

---

## 🎓 Product Philosophy

Ari explores a broader idea about AI-powered software:

> **The value of an LLM does not come only from the model itself, but from the system built around it.**

The model is only one component of the product.

Ari combines the model with:

- Domain-specific knowledge
- Retrieval infrastructure
- Ranking
- Document processing
- Persistent state
- Authentication
- Authorization
- Streaming
- Application-level business logic

This architecture allows the AI assistant to become part of an actual product experience rather than an isolated API call.

---

## 🚀 What This Project Demonstrates

Ari brings together several areas of modern software and AI engineering:

- **AI application development**
- **Agentic workflows**
- **RAG architecture**
- **Hybrid information retrieval**
- **Vector search**
- **Full-text search**
- **Reciprocal Rank Fusion**
- **Neural reranking**
- **Multimodal LLMs**
- **Tool calling**
- **Conversational state**
- **Document processing**
- **Backend architecture**
- **Authentication & authorization**
- **Asynchronous APIs**
- **Streaming responses**
- **PostgreSQL / Supabase**

Rather than focusing on a single AI technique, the project explores how these components can be combined into a coherent product.

---

## 📌 Status

Ari is an ongoing project and experimentation platform for building AI-powered educational experiences.

The current backend provides the core infrastructure for authentication, class management, material ingestion, retrieval, conversational AI, and persistent chat state.

---

<p align="center">
  Built with Python, FastAPI, LangGraph, Gemini, PostgreSQL and Supabase.
</p>
