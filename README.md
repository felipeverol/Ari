# Ari

Ari is a RAG (Retrieval-Augmented Generation) system designed for educational purposes, allowing students and educators to upload PDF or Markdown files, index them with ChromaDB, and interact via chat to ask questions and explore the content using FastAPI and LangChain with Gemini/Google Generative AI integration.

## Features

- Upload .pdf and .md files of textbooks, articles, or study materials through a web interface.
- Automatic indexing of uploaded educational content using Google Generative AI embeddings.
- Local vector database with ChromaDB for fast and accurate retrieval.
- Chat interface for asking questions and exploring learning materials interactively.
- Backend in FastAPI, simple frontend in HTML/CSS/JS.

## Project structure

```
Ari/
├── backend/
│   ├── app/
│   │   └── main.py                     # Backend FastAPI (upload, processing, and chat endpoints)
│   ├── utils/
|   |   ├── database/
|   |   |   ├── create_database.sql     # DDL functions to create database
|   |   |   └── relational_model.png    # Picture of the relational model used
│   │   └── RAG/
|   |       ├── chroma/                 # ChromaDB vector database
|   |       ├── data/                   # Folder where uploaded files are saved
│   │       ├── add_document.py         # Functions to load and index educational documents
|   |       ├── create_db.py            # Script to create the ChromaDB database
|   |       └── query_data.py           # Function to query the vector database
│   └── requirements.txt                # Project dependencies
└── frontend/
    └── index.html                      # Web interface for uploading files and chat
```

## How to use it

### 1. Install dependencies

In the project directory:

```sh
python -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt
cd ..
```

### 2. Set up the Google Gemini API Key

Add your key to the environment:

```sh
export GOOGLE_API_KEY="SUA_CHAVE_AQUI"
```

To avoid having to export every time, add it to your `~/.bashrc` or `~/.zshrc`.

### 3. Run the backend

```sh
uvicorn backend.app.main:app --reload
```

Open [http://localhost:8000/](http://localhost:8000/) in the web browser.

### 4. Use the chat

- Upload PDFs or Markdown study materials.
- After uploading, files are processed and indexed for retrieval.
- Ask questions in the chat to explore concepts, clarify doubts, or review key points from your materials.

## Notes

- Requires Python 3.12.10.
- The ChromaDB vector database and uploaded files are saved locally in RAG/chroma and RAG/data.
- Designed for educational purposes, helping students and educators interact with study content efficiently.

## Main dependecies 

See all in [`requirements.txt`](requirements.txt), but the main ones are:
- fastapi
- langchain_community, langchain_core, langchain_chroma, langchain_google_genai, langchain_text_splitters
- pypdf

---

For educational exploration, study, and interactive learning with RAG and generative AI.